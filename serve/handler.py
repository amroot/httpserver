# This file is part of bad_http.py

from http.server import SimpleHTTPRequestHandler
from serve.pretty_colors import print_color

def http_handler_options(banner):
    if banner is not None:
        SimpleHTTPRequestHandler.server_version = banner
        SimpleHTTPRequestHandler.sys_version = ""


# Setup handler - send headers based on options. 
class HTTPHandler(SimpleHTTPRequestHandler):

    def end_headers(self):
        self.send_headers()
        SimpleHTTPRequestHandler.end_headers(self)

    def send_headers(self):
        if self.cors_dynamic:
            self.send_header('Access-Control-Allow-Origin', self.headers.get('Origin'))
        
        if self.response_headers:
            for k,v in self.response_headers.items():
                self.send_header(k,v)

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_headers()
        SimpleHTTPRequestHandler.end_headers(self)