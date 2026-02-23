#!/usr/bin/env python3
from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import packaging_config


def main() -> int:
    metadata = packaging_config.load_project_metadata()
    version = metadata["version"]
    args = packaging_config.build_pyinstaller_command(version=version)
    cmd = [sys.executable, "-m", "PyInstaller", *args]

    print("Running:", " ".join(shlex.quote(part) for part in cmd))
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)

    app_path = packaging_config.patch_built_app_bundle(version=version)
    print(f"Build complete: {app_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
