#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_PNG = ROOT_DIR / "assets" / "icon-token-orbit-a-1024.png"
OUT_ICNS = ROOT_DIR / "assets" / "icon-token-orbit-a.icns"


def main() -> int:
    if not SRC_PNG.exists():
        print(f"Source PNG not found: {SRC_PNG}", file=sys.stderr)
        return 1

    OUT_ICNS.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(SRC_PNG)
    img.save(
        OUT_ICNS,
        format="ICNS",
        sizes=[(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)],
    )
    print(f"generated: {OUT_ICNS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
