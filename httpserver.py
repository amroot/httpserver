#!/usr/bin/env python3

# By Robert Gilbert (amroot.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Example self-signed cert if needed:
# openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout server.pem -out server.pem
# Lets encrypt:
# certbot certonly --standalone --agree-tos -m test@attackersite.com -d attackersite.com --dry-run

import argparse
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
import ssl
import signal
import subprocess
import sys

if sys.version_info[0] < 3:
    exit("Python 3 required")

# Setup handler... send headers based on options. 
class HTTPHandler(SimpleHTTPRequestHandler):
	def end_headers(self):
		self.send_headers()
		SimpleHTTPRequestHandler.end_headers(self)
	def send_headers(self):
		if self.cors:
			self.send_header("Access-Control-Allow-Origin", "*")
			self.send_header("Access-Control-Allow-Headers", self.headers.get('Access-Control-Request-Headers'))
			self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		if self.custom_headers:
			try:
				for custom_header in self.custom_headers:
					header = custom_header.split(":")[0]
					value = custom_header.split(":")[1]
					self.send_header(header, value)
			except IndexError as e:
				print_color("Problem with the headers passed to --headers", "e")
				exit(print_color("Error: " + str(e), "e"))
	def do_OPTIONS(self):
		self.send_response(200, "OK")
		self.send_headers()
		SimpleHTTPRequestHandler.end_headers(self)

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--banner', 
			help='Set server banner. Default is SimpleHTTP and Python version.')
	parser.add_argument('--cert', 
			help='Certificate path. Default is /opt/httpserver/server.pem.', default='/opt/httpserver/server.pem')
	parser.add_argument('--cors', action="store_true", 
			help='Sets "Access-Control-Allow-Origin=*" and supporting headers.')
	parser.add_argument('--headers', 
			help='Set or add headers. "header1:value1,header2:value2"')
	parser.add_argument('--http', action="store_true", 
			help='Use HTTP rather than HTTPS.')
	parser.add_argument('--ip', 
			help='IP address to use. Default is 0.0.0.0 aka all.')
	parser.add_argument('--port', type=int, 
			help='The port number to listen on (default is 80/http or 443/https).')
	parser.add_argument('--ufw', action="store_true", 
			help='Add firewall rules using UFW (Uncomplicated Firewall).')
	return parser.parse_args()

# Return pretty colors.  
def print_color(message, code):
    # Pretty print errors red
    if code == "e":
        print("\033[91m[!] " + message + "\033[0m")
    # Information blue
    if code == "i":
        print("\033[95m[*] " + message + "\033[0m")
    # Good green
    if code == "g":
        print("\033[92m[+] " + message + "\033[0m")
    # Warning
    if code == "w":
        print("\033[93m[*] " + message + "\033[0m")

# Add firewall rules
def ufw_add(port):
	rule = "ufw allow " + str(port) + "/tcp"
	print_color("WARNING ADDING FIREWALL: " + rule, "w")
	rule += " && ufw status"
	subprocess.call(rule, shell=True)

# Remove firewall rules
def ufw_rem(port):
	rule = "ufw delete allow " + str(port) + "/tcp"	
	print_color("Removing firewall rule: " + rule, "g")
	rule += "&& ufw status"
	subprocess.call(rule, shell=True)

# Catches Ctrl^c and exits gracefully.
# Firewall clean up is performed on "Finally" in main() 
def signal_handler(signal, frame):
	exit(0)

# Try to clean up firewall rules no matter the reason for exiting
def clean_up(ufw,port):
	# Print an extra line here so ^C isn't so ugly in output
	print()
	if ufw:
		ufw_rem(port)
	print_color("Complete.","g")

def server(http, IP, port, certfile):
	try:
	# HTTP Server
		if http:
			httpd = HTTPServer((IP, port), HTTPHandler)
			print_color("Listening on: \n" + str(httpd.server_address[0]) + ":" + str(httpd.server_port), "w")
			print_color("Ctrl^C to exit", "i")
			httpd.serve_forever()
		# HTTPS Server
		else:
				# Check if cert file exists
				cert = Path(certfile)
				if cert.is_file() is False:
					print_color("Missing certificate file.", "e")
					print_color("Hint: openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout server.pem -out server.pem", "i")
					print_color("Hint: certbot certonly --standalone --agree-tos -m test@attackersite.com -d attackersite.com --dry-run", "i")
					exit(1)
				httpd = HTTPServer((IP, port), HTTPHandler)
				httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certfile, server_side=True)
				print_color("Listening on: \n" + str(httpd.server_address[0]) + ":" + str(httpd.server_port), "w")
				print_color("Ctrl^C to exit", "i")
				httpd.serve_forever()
	except IOError as e:
		print_color("Error: " + str(e), "e")

def main():
	try:
		args = parse_args()

		# Setup listen address
		if args.ip:
			IP = args.ip
		else:
			IP = ""

		# Setup listening ports
		port = args.port
		if port:
			port = port
		elif args.http:
			port = 80
		else:
			port = 443

		# Add firewall rules if needed
		ufw = args.ufw
		if ufw:
			ufw_add(port)
		
		# Setup cert if using default HTTPS
		if args.cert:
			certfile = str(args.cert)

		# Setup banner
		if args.banner is not None:
			SimpleHTTPRequestHandler.server_version = args.banner
			SimpleHTTPRequestHandler.sys_version = ""

		# Setup CORS
		if args.cors:
			HTTPHandler.cors = True
		else:
			HTTPHandler.cors = False
		
		# Prep custom headers
		HTTPHandler.custom_headers = None
		if args.headers:
			HTTPHandler.custom_headers = args.headers.split(",")

		## Catch Ctrl^C
		signal.signal(signal.SIGINT, signal_handler)
			
		# Launch Server
		server(args.http, IP, port, certfile)
	finally:
		try:
			clean_up(ufw, port)
		except:
			pass

if __name__ == "__main__":
	main()
