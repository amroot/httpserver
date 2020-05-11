# httpserver.py
A simple python HTTP(S) server that supports CORS, Headers,  HTTP, HTTPS, and UFW.  
Like a fancy alternative to "python -m SimpleHTTPServer 8000" when more options are needed.  
Useful for creating a quick PoC related to vulnerabilities such as CSRF, XSS, etc.

## Installation
You will need to generate a certificate if you plan on using HTTPS.

#### Example self-signed cert if needed:
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout server.pem -out server.pem

#### Example of Let’s encrypt:
certbot certonly --standalone --agree-tos -m test@attackersite.com -d attackersite.com --dry-run


## Usage
```
usage: httpserver.py [-h] [--banner BANNER] [--cert CERT] [--cors] [--headers HEADERS] [--http] [--ip IP] [--port PORT] [--ufw]

optional arguments:
  -h, --help        show this help message and exit
  --banner BANNER   Set server banner. Default is SimpleHTTP and Python version.
  --cert CERT       Certificate path. Default is /opt/httpserver/server.pem.
  --cors            Sets "Access-Control-Allow-Origin=*" and supporting headers.
  --headers HEADERS Set or add headers. "header1:value1,header2:value2"
  --http            Use HTTP rather than HTTPS.
  --ip IP           IP address to use. Default is 0.0.0.0 aka all.
  --port PORT       The port number to listen on (default is 80/http or 443/https).
  --ufw             Add firewall rules using UFW (Uncomplicated Firewall).
```
