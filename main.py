#!/usr/bin/env python3
"""Validate entry.png and copy it byte-for-byte to the output directory.

Reads entry.png next to this file, checks it is a well-formed PNG (or
JPEG), within the size and dimension limits, then copies the exact
bytes to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
Deterministic: the same input always produces the same output bytes.
Exits 1 with a message on stderr when validation fails.
"""
import os
import struct
import sys
import zlib

MAX_BYTES = 1048576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def fail(message):
    print("error:", message, file=sys.stderr)
    raise SystemExit(1)


def check_png(data):
    """Full PNG structural check: chunk CRCs, required chunks in order,
    IDAT data inflates cleanly, and nothing follows the IEND chunk."""
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        fail("not a PNG file")
    pos = 8
    seen = {"IHDR": False, "IDAT": False, "IEND": False}
    idat = bytearray()
    width = height = None
    while True:
        if pos + 8 > len(data):
            fail("truncated PNG chunk header")
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 8 + length + 4
        if end > len(data):
            fail("truncated PNG chunk: %s" % kind.decode("latin-1"))
        body = data[pos + 8:pos + 8 + length]
        crc_stored, = struct.unpack(">I", data[pos + 8 + length:end])
        crc_actual = zlib.crc32(kind + body) & 0xFFFFFFFF
        if crc_stored != crc_actual:
            fail("bad CRC in %s chunk" % kind.decode("latin-1"))
        name = kind.decode("latin-1")
        if name == "IHDR":
            if seen["IHDR"] or pos != 8 or length != 13:
                fail("malformed IHDR chunk")
            width, height = struct.unpack(">II", body[:8])
            seen["IHDR"] = True
        elif name == "IDAT":
            if not seen["IHDR"]:
                fail("IDAT before IHDR")
            idat += body
            seen["IDAT"] = True
        elif name == "IEND":
            if length != 0 or not seen["IHDR"] or not seen["IDAT"]:
                fail("malformed IEND chunk")
            seen["IEND"] = True
            if end != len(data):
                fail("trailing bytes after IEND")
            break
        elif name not in seen:
            if not seen["IHDR"]:
                fail("chunk before IHDR: %s" % name)
        pos = end
    if width is None or height is None:
        fail("missing IHDR")
    try:
        zlib.decompress(bytes(idat))
    except zlib.error as exc:
        fail("IDAT does not inflate: %s" % exc)
    return width, height


def check_jpeg(data):
    """Walk JPEG markers; require SOI, a SOF frame for dimensions, and
    an EOI marker with nothing after it."""
    if len(data) < 2 or data[:2] != b"\xff\xd8":
        fail("not a JPEG file")
    pos = 2
    width = height = None
    while pos < len(data):
        if data[pos] != 0xFF:
            fail("bad JPEG marker at offset %d" % pos)
        marker = data[pos + 1]
        if marker == 0xD8:
            fail("unexpected SOI inside JPEG")
        if marker == 0xD9:
            if pos + 2 != len(data):
                fail("trailing bytes after EOI")
            if width is None:
                fail("JPEG has no frame")
            return width, height
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if pos + 4 > len(data):
            fail("truncated JPEG segment")
        seg_len, = struct.unpack(">H", data[pos + 2:pos + 4])
        if seg_len < 2 or pos + 2 + seg_len > len(data):
            fail("truncated JPEG segment")
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            if seg_len < 7:
                fail("short JPEG frame segment")
            height, width = struct.unpack(
                ">HH", data[pos + 5:pos + 9])
        if marker == 0xDA:
            # Start of scan: entropy data runs until the next marker
            # that is not a restart marker or 0x00 stuffing byte.
            pos += 2 + seg_len
            while pos + 1 < len(data):
                if data[pos] == 0xFF and data[pos + 1] != 0x00 \
                        and not 0xD0 <= data[pos + 1] <= 0xD7:
                    break
                pos += 1
            continue
        pos += 2 + seg_len
    fail("JPEG has no EOI marker")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail("cannot read %s: %s" % (source, exc))
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the %d byte limit"
             % (len(data), MAX_BYTES))
    if data[:8] == PNG_MAGIC:
        width, height = check_png(data)
    elif data[:3] == JPEG_MAGIC:
        width, height = check_jpeg(data)
    else:
        fail("entry.png is neither PNG nor JPEG")
    if width > MAX_SIDE or height > MAX_SIDE:
        fail("image is %dx%d, over the %d px side limit"
             % (width, height, MAX_SIDE))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.png")
        with open(target, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail("cannot write output: %s" % exc)
    print("ok: %dx%d, %d bytes -> %s" % (width, height, len(data), target))


if __name__ == "__main__":
    main()
