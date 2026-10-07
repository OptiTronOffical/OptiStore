"""Launch the OptiStore web app from source or a PyInstaller executable."""

from __future__ import annotations

import argparse
import http.server
import json
import os
import socket
import sys
import threading
import urllib.error
import urllib.request
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Catalogs fetched from the repository on every launch so the app always shows
# the latest data without rebuilding or redeploying.
CATALOG_FILES = (
    "export_with_covers.json",
    "games.json",
    "dlps.json",
    "pippo.json",
    "pfs.json",
)
DEFAULT_CATALOG_SOURCE = "https://raw.githubusercontent.com/OptiTronOffical/OptiStore/main/"
FETCH_TIMEOUT = 30


def app_directory() -> Path:
    """Return the folder containing the bundled static app files."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parent


def cache_directory() -> Path:
    """Return a user-writable folder for downloaded catalogs."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Caches"
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
    return base / "OptiStore" / "catalogs"


def is_valid_json(path: Path) -> bool:
    try:
        json.loads(path.read_bytes())
        return True
    except (OSError, ValueError):
        return False


def fetch_catalog(source: str, name: str, cache_dir: Path) -> tuple[str, str]:
    """Download one catalog into the cache, keeping the old copy on any failure."""
    target = cache_dir / name
    etag_file = cache_dir / f"{name}.etag"
    request = urllib.request.Request(source + name, headers={"User-Agent": "OptiStore"})
    if etag_file.is_file() and is_valid_json(target):
        request.add_header("If-None-Match", etag_file.read_text().strip())
    try:
        with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
            data = response.read()
            etag = response.headers.get("ETag")
    except urllib.error.HTTPError as exc:
        if exc.code == 304:
            return name, "up to date"
        return name, f"failed (HTTP {exc.code})"
    except (urllib.error.URLError, OSError) as exc:
        return name, f"failed ({getattr(exc, 'reason', exc)})"

    try:
        json.loads(data)
    except ValueError:
        return name, "failed (invalid JSON)"

    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(target)
    if etag:
        etag_file.write_text(etag)
    else:
        etag_file.unlink(missing_ok=True)
    return name, "updated"


def sync_catalogs(source: str, cache_dir: Path) -> None:
    """Fetch every catalog in parallel; missing ones fall back to the bundled copy."""
    if not source.endswith("/"):
        source += "/"
    cache_dir.mkdir(parents=True, exist_ok=True)
    print(f"Fetching latest catalogs from {source}")
    with ThreadPoolExecutor(max_workers=len(CATALOG_FILES)) as pool:
        results = pool.map(lambda name: fetch_catalog(source, name, cache_dir), CATALOG_FILES)
        for name, status in results:
            fallback = ""
            if status.startswith("failed"):
                fallback = " - using cached copy" if (cache_dir / name).is_file() else " - using bundled copy"
            print(f"  {name}: {status}{fallback}")


def get_lan_ip() -> str | None:
    """Find the address used for the default network route without sending data."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("192.0.2.1", 80))  # TEST-NET address; UDP connect sends nothing.
            return sock.getsockname()[0]
    except OSError:
        return None


class AppHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str, cache_dir: Path | None, **kwargs):
        self.cache_dir = cache_dir
        super().__init__(*args, directory=directory, **kwargs)

    def translate_path(self, path: str) -> str:
        # Serve a downloaded catalog in place of the bundled one when available.
        resolved = super().translate_path(path)
        if self.cache_dir is not None:
            name = Path(resolved).name
            if name in CATALOG_FILES and Path(resolved).parent == Path(self.directory):
                cached = self.cache_dir / name
                if cached.is_file():
                    return str(cached)
        return resolved

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


def make_server(host: str, preferred_port: int, directory: Path, cache_dir: Path | None):
    handler = lambda *args, **kwargs: AppHandler(  # noqa: E731
        *args, directory=str(directory), cache_dir=cache_dir, **kwargs
    )
    for port in range(preferred_port, preferred_port + 101):
        try:
            server = http.server.ThreadingHTTPServer((host, port), handler)
            server.daemon_threads = True
            return server
        except OSError:
            continue
    raise OSError(f"Could not find an available port from {preferred_port} to {preferred_port + 100}.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run OptiStore on your local network.")
    parser.add_argument("--host", default="0.0.0.0", help="Network interface to bind (default: all interfaces).")
    parser.add_argument("--port", type=int, default=8000, help="Starting port (default: 8000; tries the next 100 ports if busy).")
    parser.add_argument("--no-browser", action="store_true", help="Do not open the app in your browser.")
    parser.add_argument("--offline", action="store_true", help="Skip fetching catalogs and use the local copies only.")
    parser.add_argument(
        "--catalog-source",
        default=DEFAULT_CATALOG_SOURCE,
        help=f"Base URL the catalogs are fetched from (default: {DEFAULT_CATALOG_SOURCE}).",
    )
    args = parser.parse_args()

    directory = app_directory()
    if not (directory / "index.html").is_file():
        print(f"OptiStore files were not found in: {directory}", file=sys.stderr)
        return 1

    cache_dir: Path | None = None
    if not args.offline:
        cache_dir = cache_directory()
        try:
            sync_catalogs(args.catalog_source, cache_dir)
        except OSError as exc:
            print(f"Could not update catalogs ({exc}); using the bundled copies.")
            cache_dir = None

    try:
        server = make_server(args.host, args.port, directory, cache_dir)
    except OSError as exc:
        print(f"Unable to start OptiStore: {exc}", file=sys.stderr)
        return 1

    port = server.server_address[1]
    local_url = f"http://127.0.0.1:{port}/"
    lan_ip = get_lan_ip()
    print("OptiStore is running. Keep this window open while you use it.")
    print(f"On this computer: http://localhost:{port}/")
    if lan_ip:
        print(f"On your local network: http://{lan_ip}:{port}/")
    print("Press Ctrl+C to stop the server.")
    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(local_url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping OptiStore...")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
