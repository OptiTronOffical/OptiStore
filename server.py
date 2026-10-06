"""Launch the OptiStore web app from source or a PyInstaller executable."""

from __future__ import annotations

import argparse
import http.server
import socket
import sys
import threading
import webbrowser
from pathlib import Path


def app_directory() -> Path:
    """Return the folder containing the bundled static app files."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parent


def get_lan_ip() -> str | None:
    """Find the address used for the default network route without sending data."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("192.0.2.1", 80))  # TEST-NET address; UDP connect sends nothing.
            return sock.getsockname()[0]
    except OSError:
        return None


class AppHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


def make_server(host: str, preferred_port: int, directory: Path):
    handler = lambda *args, **kwargs: AppHandler(  # noqa: E731
        *args, directory=str(directory), **kwargs
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
    args = parser.parse_args()

    directory = app_directory()
    if not (directory / "index.html").is_file():
        print(f"OptiStore files were not found in: {directory}", file=sys.stderr)
        return 1

    try:
        server = make_server(args.host, args.port, directory)
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
