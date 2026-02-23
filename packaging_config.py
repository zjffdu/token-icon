from __future__ import annotations

import plistlib
from pathlib import Path
import tomllib

APP_SCRIPT = "app.py"
APP_NAME = "Token Icon"
BUNDLE_IDENTIFIER = "com.zjffdu.token-icon"
ICON_FILE = "assets/icon-token-orbit-a.icns"

PROJECT_ROOT = Path(__file__).resolve().parent
PYPROJECT_FILE = PROJECT_ROOT / "pyproject.toml"
DIST_DIR = PROJECT_ROOT / "dist"


def load_project_metadata() -> dict[str, str]:
    data = tomllib.loads(PYPROJECT_FILE.read_text(encoding="utf-8"))
    project = data.get("project", {})
    name = str(project.get("name", "token-icon"))
    version = str(project.get("version", "0.1.0"))
    return {"name": name, "version": version}


def get_hidden_imports() -> list[str]:
    return [
        "api",
        "config",
        "settings_window",
        "AppKit",
    ]


def get_bundle_metadata(version: str) -> dict:
    return {
        "CFBundleName": APP_NAME,
        "CFBundleDisplayName": APP_NAME,
        "CFBundleIdentifier": BUNDLE_IDENTIFIER,
        "CFBundleShortVersionString": version,
        "CFBundleVersion": version,
        # Menubar app: hide Dock icon and app switcher entry.
        "LSUIElement": True,
    }


def build_pyinstaller_command(version: str) -> list[str]:
    command = [
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        APP_NAME,
        "--icon",
        ICON_FILE,
        "--osx-bundle-identifier",
        BUNDLE_IDENTIFIER,
    ]
    for module in get_hidden_imports():
        command.extend(["--hidden-import", module])
    command.append(APP_SCRIPT)
    return command


def get_app_bundle_path() -> Path:
    return DIST_DIR / f"{APP_NAME}.app"


def patch_built_app_bundle(version: str) -> Path:
    app_path = get_app_bundle_path()
    plist_path = app_path / "Contents" / "Info.plist"
    if not plist_path.exists():
        raise FileNotFoundError(f"Bundle plist not found: {plist_path}")

    with plist_path.open("rb") as f:
        plist_data = plistlib.load(f)

    plist_data.update(get_bundle_metadata(version))

    with plist_path.open("wb") as f:
        plistlib.dump(plist_data, f)

    return app_path
