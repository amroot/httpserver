# This file is part of bad_http.py

from argparse import ArgumentParser
from os.path import abspath


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--banner', 
                    help='Set server banner. Default is SimpleHTTP and Python version.')    
    parser.add_argument('--cert', 
                    help='Certificate path. Default is /opt/bad_http/server.pem.', 
                    default='/opt/bad_http/server.pem',
                    type=abspath)
    parser.add_argument('--cors-all', action='store_true', 
                    help='Sets \'Access-Control-Allow-Origin=*\' and supporting headers.')
    parser.add_argument('--cors-static', 
                    help='Sets \'Access-Control-Allow-Origin\' to a static value' \
                        '(e.g.: \'https://example.com, http://10.0.0.10)\'.')
    parser.add_argument('--cors-dynamic',
                     action='store_true', 
                     help='[DANGEROUS] Dynamically sets \'Access-Control-Allow-Origin\'' \
                        'to any supplied request Origin.')    
    parser.add_argument('--cors-auth',
                     action='store_true',
                     help='[DANGEROUS] Sets \'Access-Control-Allow-Credentials=True\' and' \
                        'supporting headers.')
    parser.add_argument('--cors-methods',
                    help='Sets \'Access-Control-Allow-Methods\'. Note OPTIONS must always be ' \
                        'returned with CORS for pre-flight browser checks.',
                    default='GET,HEAD,OPTIONS,POST')
    parser.add_argument('--cors-headers',
                    help='[DANGEROUS] Sets \'Access-Control-Allow-Headers\'')    
    parser.add_argument('--headers', 
                    help='Set or add headers (e.g.: \'header1:value1,header2:value2\')')
    parser.add_argument('--http', action='store_true', 
                    help='Use HTTP rather than HTTPS.')
    parser.add_argument('--ip', 
                    help='IP address to use. Default is 0.0.0.0 aka all.',
                    default='0.0.0.0')
    parser.add_argument('--port', type=int, 
                    help='The port number to listen on (default is 80/http or 443/https).')
    parser.add_argument('--ufw', action='store_true', 
                    help='Add firewall rules using UFW (Uncomplicated Firewall).')
    parser.add_argument('--web-root',
                    help='Set web-root. Default is current directory.')
    return parser.parse_args()
