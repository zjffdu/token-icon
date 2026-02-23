# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                  # Install dependencies
uv run python app.py     # Run the app
pgrep -fl "app.py"       # Check if running
pkill -f "app.py"        # Kill the app
```

No test suite or linter is configured.

## Architecture

A minimal macOS menu bar app (~190 lines total) that polls a remote API and displays token quota stats.

**Files:**
- `app.py` — `TokenIconApp(rumps.App)`: menu bar UI, background threading, timer-based refresh
- `api.py` — `fetch_token_stats(token_key)`: single GET to `https://his.ppchat.vip/api/token-stats`
- `config.py` — JSON config at `~/.config/token-icon/config.json` (`token_key`, `refresh_interval`)
- `settings_window.py` — two-step settings dialog via `osascript` (AppleScript)

**Data flow:** Timer fires → background thread → `fetch_token_stats()` → update menu labels. Settings dialog saves config and restarts the timer.
