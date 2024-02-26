#!/usr/bin/env python
import sys
import socket

def main():
    args = sys.argv[1:]

    if len(args) != 2 or not args[1].isdigit():
        print("Usage: python3 zad6.py <hostname/ip> <port>")
        sys.exit(1)

    hostname = args[0]
    port = int(args[1])

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        print(f"Connected")
        sock.close()
    except ConnectionRefusedError:
        print(f"Connection refused")

if __name__ == "__main__":
    main()
