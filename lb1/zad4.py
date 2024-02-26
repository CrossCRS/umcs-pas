#!/usr/bin/env python
import sys
import socket
from zad3 import is_valid_ip

def main():
    args = sys.argv[1:]

    if len(args) != 1:
        print("Usage: python3 zad4.py <ip_address>")
        sys.exit(1)

    ip = args[0]
    if not is_valid_ip(ip):
        print("The IP address is not correct")
        sys.exit(1)

    try:
        print(f"Hostname for IP {ip} is {socket.gethostbyaddr(ip)[0]}")
    except socket.herror:
        print(f"Hostname for IP {ip} not found")

if __name__ == "__main__":
    main()
