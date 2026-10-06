#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python3 -m venv .venv-build
.venv-build/bin/python -m pip install --upgrade pyinstaller
.venv-build/bin/python -m PyInstaller --noconfirm --clean --onefile --name OptiStore \
  --add-data "index.html:." \
  --add-data "export_with_covers.json:." \
  --add-data "games.json:." \
  --add-data "ps5-catalog.json:." \
  server.py

echo "Build complete: dist/OptiStore"
echo "Run it with: ./dist/OptiStore"
