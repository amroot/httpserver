#!/usr/bin/env python

"""
Copyright 2016 Robert Gilbert - amroot.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

===================================================================

httpserver.py
	A simple python HTTP(S) server that supports UFW, HTTP, HTTPS, and CORS.

Version 0.1 - November 1, 2016
	Release

Example self-signed cert if needed:
	openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout /opt/httpserver/server.pem -out /opt/httpserver/server.pem
"""

from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer, ssl, argparse, subprocess, signal, sys

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, help='The port number to listen on (default is 80/http or 443/https).')
parser.add_argument('--http', action="store_true", help='Use HTTP rather than HTTPS.')
parser.add_argument('--cors', action="store_true", help='Sets "Access-Control-Allow-Origin=*" and supporting headers.')
parser.add_argument('--ufw', action="store_true", help='DO NOT add firewall rules using UFW (Uncomplicated Firewall).')
parser.add_argument('--ip', help='IP address to use. Default is 0.0.0.0 aka all.')
parser.add_argument('--cert', help='Certificate path. Default is /opt/httpserver/server.pem.', default='/opt/httpserver/server.pem')
parser.add_argument('--banner', help='Set server banner. Default is SimpleHTTP and Python version.')
args = parser.parse_args()

# Setup listening ports
if args.port:
	PORT = args.port
elif args.http:
	PORT = 80
else:
	PORT = 443

# Setup listen address
if args.ip:
	IP = args.ip
else:
	IP = ""

# Setup cert if using default HTTPS
if args.http is False and args.cert:
	certfile = str(args.cert)

# Pretty colors
OKGREEN = '\033[92m'
WARNING = '\033[93m'
ENDC = '\033[0m'

# Add firewall rules
def ufw_add():
	rule = "ufw allow " + str(PORT) + "/tcp"
	print "\n" + WARNING + "WARNING ADDING FIREWALL: " + rule + ENDC
	rule += " && ufw status"
	subprocess.call(rule, shell=True)

# Remove firewall rules
def ufw_rem():
		rule = "ufw delete allow " + str(PORT) + "/tcp"
		print "\n" + OKGREEN + "Removing firewall rule: " + rule + ENDC
		rule += "&& ufw status"
		subprocess.call(rule, shell=True)

# Remove firewall rules on Ctrl^c if enabled
def signal_handler(signal, frame):
	if args.ufw is False:
		ufw_rem()
	print "\n" + OKGREEN + "Complete. " + ENDC
	sys.exit(0)
		
# Catch Ctrl^C
signal.signal(signal.SIGINT, signal_handler)

# Setup handler... send headers based on options. 
class HTTPHandler(SimpleHTTPRequestHandler):
	if args.banner:
		server_version = args.banner
		sys_version = ""
	def end_headers(self):
		self.send_headers()
		SimpleHTTPRequestHandler.end_headers(self)
	def send_headers(self):
		if args.cors:
			self.send_header("Access-Control-Allow-Origin", "*")
			self.send_header("Access-Control-Allow-Headers", self.headers.get('Access-Control-Request-Headers'))
			self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
	def do_OPTIONS(self):
		self.send_response(200, "OK")
		self.send_headers()
		SimpleHTTPRequestHandler.end_headers(self)

# Displays IP address helper
if args.ip is None:
	hostip = str(subprocess.check_output(["hostname", "-I"]))
	print "\nKnown IP addresses on this host:\n" + hostip

# HTTP Server
if args.http:
	httpd = BaseHTTPServer.HTTPServer((IP, PORT), HTTPHandler)
	print WARNING + "Listening on: \n" + str(httpd.server_address[0]) + ":" + str(httpd.server_port) + ENDC
	print "\nCtrl^C to exit"
	if args.ufw is False:
		ufw_add()
	httpd.serve_forever()
# HTTPS Server
else:
	try:
		httpd = BaseHTTPServer.HTTPServer((IP, PORT), HTTPHandler)
		httpd.socket = ssl.wrap_socket (httpd.socket, certfile=certfile, server_side=True)
		print WARNING + "Listening on: \n" + str(httpd.server_address[0]) + ":" + str(httpd.server_port) + ENDC
		print "\nCtrl^C to exit"
		if args.ufw is False:
			ufw_add()
		httpd.serve_forever()
	except IOError:
		print WARNING + "Missing cert?\n"
		parser.print_help()
		print ENDC
