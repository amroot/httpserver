# This file is part of bad_http.py

from http.server import HTTPServer
from serve.handler import HTTPHandler
from serve.pretty_colors import print_color
from ssl import PROTOCOL_TLS_SERVER
from ssl import SSLContext
from threading import Thread


class Server:
    def __init__(self):
        self.httpd = None
        self.server_thread = None

    def listen(self, http, IP, port, certfile):
        try:
            self.httpd = HTTPServer((IP, port), HTTPHandler)
            if not http:
                context = SSLContext(PROTOCOL_TLS_SERVER)
                context.load_cert_chain(certfile=certfile)  
                self.httpd.socket = context.wrap_socket(self.httpd.socket, server_side=True)
            print_color(f'Listening on:\n{str(self.httpd.server_address[0])}:{str(self.httpd.server_port)}', 'g')
            print_color('Ctrl^C to exit', 'i')
            
            # Create and start server thread
            self.server_thread = Thread(target=self.httpd.serve_forever)
            self.server_thread.daemon = True  # Thread will exit when main program does
            self.server_thread.start()
            
            # Wait for the thread to complete when shutdown is called
            self.server_thread.join()
            
        except IOError as e:
            print_color(f'Error: {str(e)}', 'e')
            exit(1)

    def shutdown(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()