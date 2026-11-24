#!/usr/bin/env python3
"""Write the 24 November 2026 front page to /output/entry.png.

The picture lives in this repository as base64 text (entry.png.b64).
Decoding it is deterministic: the same bytes in, the same bytes out.
Standard library only, no network.
"""

import os
from base64 import b64decode
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_FILE = HERE / "entry.png.b64"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    raw = DATA_FILE.read_bytes()
    picture = b64decode(raw)
    if picture[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png.b64 does not decode to a PNG")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "entry.png").write_bytes(picture)


if __name__ == "__main__":
    main()
