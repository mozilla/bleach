#!/usr/bin/env python

"""
Simple Test/Demo Server for running bleach.clean output on various
desktops.

Usage:

    python server.py

"""

import six

import bleach


PORT = 8080


class BleachCleanHandler(six.moves.SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        if six.PY2:
            content_len = int(self.headers.getheader('content-length', 0))
        else:
            content_len = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_len)
        print("read %s bytes: %s" % (content_len, body))

        if six.PY3:
            body = body.decode('utf-8')
        print('input: %r' % body)
        cleaned = bleach.clean(body)

        self.send_response(200)
        self.send_header('Content-Length', len(cleaned))
        self.send_header('Content-Type', 'text/plain;charset=UTF-8')
        self.end_headers()

        if six.PY3:
            cleaned = bytes(cleaned, encoding='utf-8')
        print("cleaned: %r" % cleaned)
        self.wfile.write(cleaned)


if __name__ == '__main__':
    # Prevent 'cannot bind to address' errors on restart
    six.moves.socketserver.TCPServer.allow_reuse_address = True

    httpd = six.moves.socketserver.TCPServer(('127.0.0.1', PORT), BleachCleanHandler)
    print("listening on localhost port %d" % PORT)
    httpd.serve_forever()
