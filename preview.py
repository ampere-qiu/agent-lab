"""Serve the built docs on loopback without hostname lookups."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from socketserver import TCPServer


class PreviewHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        # Always show rebuilt lessons, including files rebuilt within one second.
        for header in ("If-Modified-Since", "If-None-Match"):
            if header in self.headers:
                del self.headers[header]
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class LocalServer(ThreadingHTTPServer):
    def server_bind(self):
        TCPServer.server_bind(self)
        self.server_name = "localhost"
        self.server_port = self.server_address[1]


if __name__ == "__main__":
    handler = partial(PreviewHandler, directory=str(Path(__file__).parent / "site"))
    with LocalServer(("127.0.0.1", 8003), handler) as server:
        print("Preview: http://127.0.0.1:8003/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
