# httpserver
A simple python HTTP(S) server that supports UFW, HTTP, HTTPS, and CORS.  
Like a fancy alternative to "python -m SimpleHTTPServer 8000" when more options are needed.  
Useful for creating a quick PoC related to vulnerabilities such as CSRF, XSS, etc.  

## usage
usage: httpserver.py [-h] [--port PORT] [--http] [--cors] [--ufw] [--ip IP] [--cert CERT] [--banner BANNER]  

optional arguments:  
  -h, --help       show this help message and exit  
  --port PORT      The port number to listen on (default is 80/http or 443/https).  
  --http           Use HTTP rather than HTTPS.  
  --cors           Sets "Access-Control-Allow-Origin=*" and supporting headers.  
  --ufw            DO NOT add firewall rules using UFW (Uncomplicated Firewall).  
  --ip IP          IP address to use. Default is 0.0.0.0 aka all.  
  --cert CERT      Certificate path. Default is /opt/httpserver/server.pem.  
  --banner BANNER  Set server banner. Default is SimpleHTTP and Python version.
