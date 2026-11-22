#!/usr/bin/env python3
"""news-image-20261122 entry: sum up Sunday 22 November 2026's world news.

The entry is the bundled front-page image (entry.png, 1024x1024). It was
drawn from real reporting of 22 Nov 2026: Bitcoin climbing back above
$60,000 after a two-year low, three tankers hit near the Strait of Hormuz,
the G20 summit in Johannesburg, COP31's final day, Russian missiles landing
in Poland, and 43 sourced stories in all, with a UTC timeline and a
markets panel. This program just places that image at /output/entry.png.

Standard library only, no network, fully deterministic: every run copies
the same bundled bytes, so two runs write identical files.
"""

import os
import shutil
import sys

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def run():
    base = os.path.dirname(os.path.abspath(__file__))
    bundled = os.path.join(base, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(bundled, target)

    with open(target, "rb") as handle:
        head = handle.read(len(PNG_MAGIC))
        handle.seek(-12, os.SEEK_END)
        tail = handle.read(12)
    if head != PNG_MAGIC:
        raise SystemExit("entry.png does not start with a PNG signature")
    if tail != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        raise SystemExit("entry.png does not end with a whole PNG IEND chunk")
    size = os.path.getsize(target)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB cap")
    print(f"wrote {target} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
