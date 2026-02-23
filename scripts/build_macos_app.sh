#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

uv run --with pillow python scripts/make_icns_from_png.py

echo "Building macOS app bundle with PyInstaller..."
uv run --with pyinstaller python scripts/build_macos_app.py

echo "Build complete."
echo "App bundle: dist/Token Icon.app"
