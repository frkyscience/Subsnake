# Imports
from colorama import Fore
import requests
import argparse
from dns import resolver
import sys
import os
from os import path
import socket
from concurrent.futures import ThreadPoolExecutor

# ASCII art
ascii_art = r'''
       ---_ ......._-_--.
      (|\ /      / /| \
      /  /     .'  -=-'   .
     /  /    .'             )
   _/  /   .'        _.)   /
  / o   o        _.-' /  .'
  \          _.-'    / .'*|
   \______.-'//    .'.' \*|
    \|  \ | //   .'.' _ |*|
        \|//  .'.'_ _ _|*|
      .  .// .'.'
      \-|\_/ /
       /'\__/
      /^|
     '        __                     __
   _______  __/ /_  _________  ____ _/ /_____
  / ___/ / / / __ \/ ___/ __ \/ __ / //_/ _ \
 (__  ) /_/ / /_/ (__  ) / / / /_/ / ,< /  __/
/____/\__,_/_.___/____/_/ /_/\__,_/_/|_|\___/  v0.3.1 by Jb
'''

# Print the ASCII art
print(Fore.GREEN + ascii_art)

def query_subdomains(domain):
    """Query for subdomains using a list of predefined subdomains."""
    subdomains = [
        "www", "mail", "ftp", "localhost", "webmail", "smtp", "blog", "webdisk",
        "ns1", "ns2", "cpanel", "whm", "autodiscover", "admin", "secure", "vpn",
        "shop", "api", "test", "dev", "demo", "imap", "pop", "support", "billing",
        "helpdesk", "login", "portal", "owa", "gateway", "firewall", "proxy",
        "router", "monitor", "backup", "cache", "cdn", "storage", "db", "database",
        "staging", "forums", "wiki", "download", "assets", "cdn", "en", "app", "cashier"
    ]
    found_subdomains = []

    for sub in subdomains:
        try:
            full_domain = f"{sub}.{domain}"
            answers = resolver.resolve(full_domain, 'A')
            for rdata in answers:
                found_subdomains.append(full_domain)
                print(Fore.GREEN + f"Found: {full_domain}")
        except resolver.NXDOMAIN:
            pass
        except Exception as e:
            print(Fore.RED + f"Error resolving {full_domain}: {str(e)}")

    return found_subdomains

def query_crtsh(domain):
    """Query crt.sh for subdomains."""
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            subdomains = set()
            for entry in response.json():
                name = entry.get('name_value')
                if name:
                    subdomains.update(name.split('\n'))
            return list(subdomains)
        else:
            print(Fore.RED + f"Error querying crt.sh: {response.status_code}")
            return []
    except Exception as e:
        print(Fore.RED + f"Error querying crt.sh: {str(e)}")
        return []

def save_to_file(filename, subdomains):
    """Save the subdomains to a file."""
    with open(filename, "a") as file:
        for subdomain in subdomains:
            file.write(subdomain + "\n")

def colorize_status_code(status_code):
    """Return colorized status code based on its class."""
    class_code = status_code // 100  # Get the class of the status code (2, 3, 4, etc.)
    color_map = {
        2: Fore.GREEN,   # 2xx codes (Successful)
        3: Fore.YELLOW,  # 3xx codes (Redirection)
        4: Fore.RED      # 4xx codes (Client Error)
    }
    color = color_map.get(class_code, Fore.RESET)  # Get color from the map, default to reset color
    return color + str(status_code)

def probe_status_codes(subdomains):
    """Probe and print HTTP status codes and headers for each subdomain with color coding."""
    for subdomain in subdomains:
        print(f"{Fore.CYAN}Subdomain: {subdomain}")

        # Safely split the subdomain and handle cases where there are fewer parts
        domain_parts = subdomain.split('.')
        if len(domain_parts) >= 2:
            # Assume the last two parts are the domain (e.g., 'example.com')
            base_domain = f"{domain_parts[-2]}.{domain_parts[-1]}"
        else:
            base_domain = subdomain  # In case there's no valid split, fall back to the full subdomain

        # Resolve IP for the base domain
        ip = get_domain_ip(base_domain)
        if ip:
            print(Fore.GREEN + f"Resolved IP: {ip}")

            # Scan for open ports on the resolved IP
            open_ports = scan_ports(ip)
            if open_ports:
                print(Fore.GREEN + f"Open ports on {ip}: {', '.join(map(str, open_ports))}")
            else:
                print(Fore.RED + f"No open ports found on {ip}")

        # Probe HTTP and HTTPS status codes
        try:
            url = f"http://{subdomain}"
            response = requests.get(url, timeout=5, verify=True)
            print(f"{Fore.CYAN}{subdomain} - HTTP Status code: {colorize_status_code(response.status_code)}")
            print(Fore.WHITE + "HTTP Headers:")
            for header, value in response.headers.items():
                print(f"  {header}: {value}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}{subdomain} - Error: {str(e)}")

        try:
            url_https = f"https://{subdomain}"
            response_https = requests.get(url_https, timeout=5, verify=True)
            print(f"{Fore.CYAN}{subdomain} - HTTPS Status code: {colorize_status_code(response_https.status_code)}")
            print(Fore.WHITE + "HTTPS Headers:")
            for header, value in response_https.headers.items():
                print(f"  {header}: {value}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}{subdomain} - Error: {str(e)}")

        print()  # Add spacing between subdomains


def get_domain_ip(domain):
    """Resolve and return the IP address of the domain."""
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        print(Fore.RED + f"Unable to resolve IP for {domain}")
        return None


def scan_ports(ip):
    """Scan the given IP for open ports."""
    ports = [80, 443, 22, 21, 25, 8080, 8443, 3306, 53, 110, 143]
    open_ports = []

    def check_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_port, ports)

    return open_ports


def probe_status_codes(subdomains):
    """Probe and print HTTP status codes and headers for each subdomain with color coding."""
    for subdomain in subdomains:
        print(f"{Fore.CYAN}Subdomain: {subdomain}")

        # Resolve IP for the subdomain
        ip = get_domain_ip(subdomain.split('.')[1] + '.' + subdomain.split('.')[2])
        if ip:
            print(Fore.GREEN + f"Resolved IP: {ip}")

            # Scan for open ports on the resolved IP
            open_ports = scan_ports(ip)
            if open_ports:
                print(Fore.GREEN + f"Open ports on {ip}: {', '.join(map(str, open_ports))}")
            else:
                print(Fore.RED + f"No open ports found on {ip}")

        # Probe HTTP and HTTPS status codes
        try:
            url = f"http://{subdomain}"
            response = requests.get(url, timeout=5, verify=True)
            print(f"{Fore.CYAN}{subdomain} - HTTP Status code: {colorize_status_code(response.status_code)}")
            print(Fore.WHITE + "HTTP Headers:")
            for header, value in response.headers.items():
                print(f"  {header}: {value}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}{subdomain} - Error: {str(e)}")

        try:
            url_https = f"https://{subdomain}"
            response_https = requests.get(url_https, timeout=5, verify=True)
            print(f"{Fore.CYAN}{subdomain} - HTTPS Status code: {colorize_status_code(response_https.status_code)}")
            print(Fore.WHITE + "HTTPS Headers:")
            for header, value in response_https.headers.items():
                print(f"  {header}: {value}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}{subdomain} - Error: {str(e)}")

        print()  # Add spacing between subdomains


def main(domain, save=None, probe=False, scan_ip_ports=False):
    # Query subdomains
    found_subdomains = query_subdomains(domain)
    crtsh_subdomains = query_crtsh(domain)
    all_subdomains = set(found_subdomains + crtsh_subdomains)

    # Probe subdomains if required
    if probe:
        probe_status_codes(all_subdomains)

    # Save to file if required
    if save and save.endswith(".txt"):
        save_to_file(save, all_subdomains)
        if path.exists(save):
            print(Fore.GREEN + "DONE! Results saved to {}".format(save))
        else:
            print(Fore.RED + "ERROR! Could not save results.")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subsnake: The Ultimate Subdomain Enumeration Tool",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-s", required=True, help="Domain to enumerate subdomains for")
    parser.add_argument("--save", help="File to save the subdomains to (optional)")
    parser.add_argument("-pc", action="store_true", help="Probe subdomains for HTTP status codes")
    parser.add_argument("-ipp", action="store_true", help="Resolve domain IP and scan for open ports")
    args = parser.parse_args()

    main(args.s, args.save, args.pc, args.ipp)
