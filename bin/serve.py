#!/usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import ssl

build_dir = os.path.dirname(os.path.realpath(__file__)) + '/../build'
cert_dir = os.path.dirname(os.path.realpath(__file__)) + '/../data/dev_cert/'

os.chdir(build_dir)

httpd = HTTPServer(('localhost', 1337), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile=cert_dir + 'key.pem',
        certfile=cert_dir + 'cert.pem', server_side=True)

httpd.serve_forever()
