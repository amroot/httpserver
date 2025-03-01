# bad_http.py

> :warning: **The server intentionally has dangerous configuration options.** Especially with CORS. This was created for educational and PoC purposes and should never be used in production.

## Description
A simple python HTTP(S) server that supports CORS, Headers,  HTTP, HTTPS, and Uncomplicated Firewall (UFW).  
Like a fancy alternative to "python -m SimpleHTTPServer 8000" when more options are needed.  
Useful for creating a quick PoC related to vulnerabilities such as CSRF, XSS, etc.

## Installation
You will need to generate a certificate if you plan on using HTTPS.

#### Example self-signed cert if needed:
New x509_cert_generator.py: https://github.com/amroot/x509_cert_generator

```
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout server.pem -out server.pem
```
#### Example of Let’s encrypt:
```
certbot certonly --standalone --agree-tos -m test@attackersite.com -d attackersite.com --dry-run
```

## Usage
```
usage: bad_http.py [-h] [--banner BANNER] [--cert CERT] [--cors-all] [--cors-static CORS_STATIC] [--cors-dynamic] [--cors-auth] [--cors-methods CORS_METHODS]
                   [--cors-headers CORS_HEADERS] [--headers HEADERS] [--http] [--ip IP] [--port PORT] [--ufw] [--web-root WEB_ROOT]

options:
  -h, --help            show this help message and exit
  --banner BANNER       Set server banner. Default is SimpleHTTP and Python version.
  --cert CERT           Certificate path. Default is /opt/bad_http/server.pem.
  --cors-all            Sets "Access-Control-Allow-Origin=*" and supporting headers.
  --cors-static CORS_STATIC
                        Sets "Access-Control-Allow-Origin" to a static value(e.g.: "https://example.com, http://10.0.0.10).
  --cors-dynamic        [DANGEROUS] Dynamically sets "Access-Control-Allow-Origin"to any supplied request Origin.
  --cors-auth           [DANGEROUS] Sets "Access-Control-Allow-Credentials=True" andsupporting headers.
  --cors-methods CORS_METHODS
                        Sets "Access-Control-Allow-Methods". Note OPTIONS must always be returned with CORS for pre-flight browser checks.
  --cors-headers CORS_HEADERS
                        [DANGEROUS] Sets "Access-Control-Allow-Headers"
  --headers HEADERS     Set or add headers (e.g.: "header1:value1,header2:value2")
  --http                Use HTTP rather than HTTPS.
  --ip IP               IP address to use. Default is 0.0.0.0 aka all.
  --port PORT           The port number to listen on (default is 80/http or 443/https).
  --ufw                 Add firewall rules using UFW (Uncomplicated Firewall).
  --web-root WEB_ROOT   Set web-root. Default is current directory.
```
