#!/usr/bin/env python3

# bad_http.py
# 
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


from os import chdir
from pathlib import Path
from serve.http_server import Server
from serve.pretty_colors import print_color
from sys import version_info
import serve.args
import serve.firewall
import serve.handler
import signal


if version_info[0] < 3:
    exit('Python 3 required')


def validate_cors_methods(methods):
    valid_methods = {
        'DELETE', 
        'GET', 
        'HEAD', 
        'OPTIONS', 
        'PATCH',
        'POST', 
        'PUT'
        }
    method_list = {m.strip().upper() for m in methods.split(',')}
    if not method_list.issubset(valid_methods):
        print_color(f'Invalid CORS methods: {methods}', 'e')
        exit(1)
    return methods.upper()


def main():
    # Catches Ctrl^c and exits gracefully.
    # and cleans up the firewall rules
    def clean_up_ufw(port):
        print_color('Removing firewall rules.', 'i')
        serve.firewall.ufw_rem(port)

    def signal_handler(signal, frame):
        # Print an extra line here so ^C isn't so ugly in output
        print()
        print_color('Shutting down the server.', 'i')
        server.shutdown()
        if args.ufw:
            clean_up_ufw(port)
        print_color('Complete.','g')
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    try:
        args = serve.args.parse_args()
        # Setup listen address
        IP = args.ip
        # Setup listening ports
        if args.port:
            port = args.port
        elif args.http:
            port = 80
        else:
            port = 443

        # Setup cert if using default HTTPS        
        if not args.http:            
            # Check if cert file exists
            certfile = str(args.cert)
            cert = Path(certfile)
            if cert.is_file() is False:
                print_color('Missing certificate file.', 'e')
                print_color('Hint: openssl req -newkey rsa:2048 -new -nodes ' \
                    '-x509 -days 3650 -keyout server.pem -out server.pem', 'i')
                print_color('Hint: certbot certonly --standalone --agree-tos ' \
                    '-m test@attackersite.com -d attackersite.com --dry-run', 'i')
                exit(1)
        # Prep headers
        headers = {}
        # Handler options
        if args.banner is not None:
            serve.handler.http_handler_options(args.banner)
        # CORS
        cors_enabled = 0
        if args.cors_all:
            headers['Access-Control-Allow-Origin'] = '*'
            cors_enabled += 1
        if args.cors_static:
            headers['Access-Control-Allow-Origin'] = args.cors_static
            cors_enabled += 1
        serve.handler.HTTPHandler.cors_dynamic = False
        if args.cors_dynamic:
            print_color('Setting Access-Control-Allow-Origin to dynamically ' \
                'match a requesting origin is extremely dangerous.\nEspecially ' \
                'when combined with \'Access-Control-Allow-Credentials\'' \
                'and/or \'Access-Control-Allow-Headers\'', 'w')
            # This must be handled by the handler to get the origin header
            serve.handler.HTTPHandler.cors_dynamic = True
            cors_enabled += 1
        if cors_enabled > 1:
            print_color('There can only be one --cors-all, --cors-dynamic, or --cors-static', 'e')
            exit(1)

        if cors_enabled and args.cors_auth:
            print_color('Setting Access-Control-Allow-Credentials will trust ' \
                'and pass auth to any domain in Access-Control-Allow-Origin', 'w')
            headers['Access-Control-Allow-Credentials'] = 'true'

        if cors_enabled and args.cors_headers:
            print_color('Setting Access-Control-Allow-Headers to include \'Authorization\' ' \
                'will pass auth to any domain in Access-Control-Allow-Origin', 'w')
            headers['Access-Control-Allow-Headers'] = args.cors_headers

        if cors_enabled:
            verbs = validate_cors_methods(args.cors_methods)
            if 'OPTIONS' not in verbs:
                print_color('Missing \'OPTIONS\' in cors-methods', 'e')
                exit(1)
            headers['Access-Control-Allow-Methods'] = verbs

        # Custom headers
        if args.headers:
            try:
                for header in args.headers.split(','):
                    k,v = header.split(':')
                    headers[k] = v
            except Exception as e:
                print_color('Problem with the headers passed to --headers', 'e')
                print_color(f'Error: {str(e)}', 'e')
                exit(1)

        serve.handler.HTTPHandler.response_headers = headers

        if args.web_root:
            chdir(args.web_root)

        # Add firewall rules if needed
        if args.ufw:
            serve.firewall.ufw_add(port)
            
        # Launch Server
        server = Server()
        server.listen(args.http, IP, port, str(args.cert))
        
    except Exception as e:
        if args.ufw:
            clean_up_ufw(port)
        print_color(f'Error: {str(e)}', 'e')
        exit(1) 


if __name__ == '__main__':
    main()