"""Build a standalone OptiStore executable for the current OS with PyInstaller.

Requires PyInstaller: python -m pip install pyinstaller
"""

import os
import sys

import PyInstaller.__main__

# Static app files bundled into the executable. The catalogs are only an
# offline fallback; the launcher fetches the latest ones on every start.
DATA_FILES = (
    "index.html",
    "ps5.html",
    "export_with_covers.json",
    "games.json",
    "dlps.json",
    "pippo.json",
    "pfs.json",
)


def main() -> None:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    missing = [name for name in DATA_FILES if not os.path.isfile(name)]
    if missing:
        sys.exit(f"Missing files: {', '.join(missing)}")

    args = ["--noconfirm", "--clean", "--onefile", "--name", "OptiStore"]
    for name in DATA_FILES:
        args += ["--add-data", f"{name}{os.pathsep}."]
    PyInstaller.__main__.run(args + ["server.py"])


if __name__ == "__main__":
    main()
