#!/usr/bin/env python

"""
Simple Test/Demo Server for running bleach.clean output on various
desktops.

Usage:

    python server.py

"""

import http.server
import socketserver

import bleach


PORT = 8080


class BleachCleanHandler(http.server.SimpleHTTPRequestHandler):

    # Prevent 'cannot bind to address' errors on restart
    allow_reuse_address = True

    def do_POST(self):
        content_len = int(self.headers.get("content-length", 0))
        body = self.rfile.read(content_len)
        print("read {} bytes: {}".format(content_len, body))

        body = body.decode("utf-8")
        print("input: %r" % body)
        cleaned = bleach.clean(body)

        self.send_response(200)
        self.send_header("Content-Length", len(cleaned))
        self.send_header("Content-Type", "text/plain;charset=UTF-8")
        self.end_headers()

        cleaned = bytes(cleaned, encoding="utf-8")
        print("cleaned: %r" % cleaned)
        self.wfile.write(cleaned)


if __name__ == "__main__":
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), BleachCleanHandler)
    print("listening on localhost port %d" % PORT)
    httpd.serve_forever()
