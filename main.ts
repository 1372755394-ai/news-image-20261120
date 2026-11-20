// Entry point for news-image-20261120.
//
// Copies the committed front page (entry.png) into MAKEFUN_OUTPUT_DIR
// (default /output) after verifying it is a well-formed 1024x1024 PNG
// under 1 MiB. A bad image is never written: every check runs before the
// copy, and the copy is read back and compared byte for byte.
//
// Node 22, standard library only. No network access, no secrets.

import { copyFile, mkdir, readFile, stat } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1_000_000;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

const here = path.dirname(fileURLToPath(import.meta.url));
const sourcePath = path.join(here, "entry.png");

function fail(message: string): never {
  throw new Error(`entry.png rejected: ${message}`);
}

function readU32BE(bytes: Buffer, offset: number): number {
  return bytes.readUInt32BE(offset);
}

/** Parse the PNG header and return its declared width and height. */
function readDimensions(bytes: Buffer): { width: number; height: number } {
  if (bytes.length < 8 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail("missing PNG signature");
  }
  if (bytes.length < 33) {
    fail("file too short to contain an IHDR chunk");
  }
  const ihdrLength = readU32BE(bytes, 8);
  const ihdrType = bytes.toString("latin1", 12, 16);
  if (ihdrLength !== 13 || ihdrType !== "IHDR") {
    fail("first chunk is not a 13-byte IHDR");
  }
  return {
    width: readU32BE(bytes, 16),
    height: readU32BE(bytes, 20),
  };
}

// CRC-32 (IEEE 802.3) table, built once at load; Node has no built-in
// CRC-32, so the table is computed here from the standard polynomial.
const CRC_TABLE: Uint32Array = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(bytes: Buffer): number {
  let crc = 0xffffffff;
  for (const byte of bytes) {
    crc = CRC_TABLE[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

/**
 * Walk every chunk from IHDR to IEND, verifying each chunk's CRC, and
 * require the file to end exactly at IEND (no trailing bytes). Returns
 * the chunk types in order so callers can also require image data.
 */
function verifyChunks(bytes: Buffer): string[] {
  const types: string[] = [];
  let offset = 8;
  for (;;) {
    if (offset + 8 > bytes.length) {
      fail("chunk header runs past end of file");
    }
    const length = readU32BE(bytes, offset);
    const type = bytes.toString("latin1", offset + 4, offset + 8);
    const dataStart = offset + 8;
    const dataEnd = dataStart + length;
    const crcEnd = dataEnd + 4;
    if (crcEnd > bytes.length) {
      fail(`chunk ${type} runs past end of file`);
    }
    if (readU32BE(bytes, dataEnd) !== crc32(bytes.subarray(offset + 4, dataEnd))) {
      fail(`chunk ${type} has a bad CRC`);
    }
    types.push(type);
    offset = crcEnd;
    if (type === "IEND") {
      if (offset !== bytes.length) fail("trailing bytes after IEND");
      break;
    }
  }
  return types;
}

function sha256(bytes: Buffer): string {
  return createHash("sha256").update(bytes).digest("hex");
}

async function main(): Promise<void> {
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const outputPath = path.join(outputDir, "entry.png");

  const bytes = await readFile(sourcePath);
  if (bytes.length >= MAX_BYTES) {
    fail(`${bytes.length} bytes, at or over the 1 MiB limit`);
  }
  const { width, height } = readDimensions(bytes);
  if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
    fail(`dimensions ${width}x${height}, expected 1024x1024`);
  }
  const chunkTypes = verifyChunks(bytes);
  if (!chunkTypes.includes("IDAT")) {
    fail("no IDAT chunk (no image data)");
  }

  await mkdir(outputDir, { recursive: true });
  await copyFile(sourcePath, outputPath);

  const copied = await readFile(outputPath);
  if (!copied.equals(bytes)) {
    fail("copy differs from source");
  }
  const copiedStat = await stat(outputPath);

  console.log(
    `wrote ${outputPath}: ${width}x${height} PNG, ` +
      `${copiedStat.size} bytes, sha256 ${sha256(copied)}`,
  );
}

await main();
