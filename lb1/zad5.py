#!/usr/bin/env python
import sys
import socket

def main():
    args = sys.argv[1:]

    if len(args) != 1:
        print("Usage: python3 zad5.py <hostname>")
        sys.exit(1)

    hostname = args[0]

    try:
        print(f"IP for hostname {hostname} is {socket.gethostbyaddr(hostname)[2][0]}")
    except socket.herror:
        print(f"IP for hostname {hostname} not found")

if __name__ == "__main__":
    main()
