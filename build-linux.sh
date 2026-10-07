#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python3 -m venv .venv-build
.venv-build/bin/python -m pip install --upgrade pyinstaller
.venv-build/bin/python build.py

echo "Build complete: dist/OptiStore"
echo "Run it with: ./dist/OptiStore"
