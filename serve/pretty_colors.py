# This file is part of bad_http.py

# Return pretty colors.  
def print_color(message, code):
    """
    Prints pretty colors.
    param message: a list or string. Honors new lines ('\\n')
    param code:
        e: error / red
        i: informational / blue
        g: good / green
        w: warning / yellow
    """

    if '\n' in message:
        message = message.split('\n')
        # removes empty lines
        message = [x for x in message if x]
    
    if message.__class__ != list:
        message = [message]
    
    for m in message:
        # Pretty print errors red
        if code == 'e':
            print(f'\033[91m[!] {m}\033[0m')
        # Information blue
        if code == 'i':
            print(f'\033[95m[*] {m}\033[0m')
        # Good green
        if code == 'g':
            print(f'\033[92m[+] {m}\033[0m')
        # Warning
        if code == 'w':
            print(f'\033[93m[*] {m}\033[0m')