#!/usr/bin/env python3
"""Generate a small `config.js` that exposes `window.apiKey` from environment or .env.

Usage:
  - Put `API_KEY=your_key` in a `.env` file (not checked in), or set the `API_KEY` env var.
  - Run: `python generate_config.py` to write `config.js`.
"""
import os
from pathlib import Path


def load_dotenv(path: Path) -> dict:
    vals = {}
    if not path.exists():
        return vals
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            vals[k.strip()] = v
    return vals


def main() -> int:
    env = dict(os.environ)
    env_path = Path(".env")
    env.update(load_dotenv(env_path))

    api_key = env.get("API_KEY", "")

    # Escape backslashes and quotes
    api_key_escaped = api_key.replace('\\', '\\\\').replace('"', '\\"')

    content = f'window.apiKey = "{api_key_escaped}";\n'
    Path("config.js").write_text(content, encoding="utf-8")
    print(f"Wrote config.js (API_KEY set: {'yes' if api_key else 'no'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
