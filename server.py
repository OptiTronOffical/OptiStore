import http.server
import socket
import socketserver

PORT = 8000


def get_local_ip():
    """Finds the local IP address of the device on the network."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Prevent browser caching so files update immediately
        self.send_header(
            "Cache-Control", "no-cache, no-store, must-revalidate"
        )
        super().end_headers()


def start_server():
    local_ip = get_local_ip()

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print("=" * 50)
        print("🚀 Local File Server is Running!")
        print("-" * 50)
        print(f"📍 Access on this computer: http://localhost:{PORT}")
        print(f"📱 Access from other devices: http://{local_ip}:{PORT}")
        print("-" * 50)
        print("Press Ctrl+C to stop the server.")
        print("=" * 50)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server. Goodbye!")


if __name__ == "__main__":
    start_server()