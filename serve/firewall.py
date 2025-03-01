# This file is part of bad_http.py

from serve.pretty_colors import print_color
from subprocess import run

# Firewall status
def firewall_status():
    status = run(['ufw', 'status'], capture_output=True)
    print_color(status.stdout.decode(), 'i')
    if b'inactive' in status.stdout:
        print_color('UFW IS INACTIVE. Run \'ufw enable\' to enable it.', 'w')
    return

# Add firewall rules
def ufw_add(port):
    rule = ['ufw', 'allow', str(port)]
    print_color(f"ADDING FIREWALL RULE: {' '.join(rule)}", "w")
    response = run(rule, capture_output=True)
    print_color(response.stdout.decode(), 'i')
    print_color(f"Added firewall rule: {' '.join(rule)}", "g")
    firewall_status()
    if b'existing' in response.stdout:
        print_color('EXISTING FIREWALL RULES IDENTIFIED. ' \
                    '\nThe existing rules will be removed during UFW clean up ' \
                    '\nYou must manually add them back if you need them.', 'e')
    return 

# Remove firewall rules
def ufw_rem(port):
    rule = ['ufw', 'delete', 'allow', str(port)]
    response = run(rule, capture_output=True)
    print_color(response.stdout.decode(), 'i')
    print_color(f"Removed firewall rule: {' '.join(rule)}", "g")
    firewall_status()
    return