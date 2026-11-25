#!/usr/bin/env python3
"""Write the championship one-liner to the harness output file.

The line itself lives in entry.txt next to this script (the prepared,
panel-winning entry). This program only moves those exact bytes to the
place the scorer reads, after checking the gate limits.
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 140


def load_entry() -> bytes:
    """Read the prepared line and check it against the gate rules."""
    source = Path(__file__).resolve().parent / "entry.txt"
    raw = source.read_bytes()
    text = raw.decode("utf-8")
    if not text.strip():
        raise SystemExit("entry.txt is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise SystemExit(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    return raw


def main() -> int:
    raw = load_entry()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(raw)
    # Read back what landed on disk: a silent short write must never
    # pass as a valid entry.
    written = target.read_bytes()
    if written != raw:
        raise SystemExit(
            f"read-back mismatch: wrote {len(raw)} bytes, "
            f"found {len(written)} bytes in {target}"
        )
    print(f"wrote {len(raw)} bytes to {target} (verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
