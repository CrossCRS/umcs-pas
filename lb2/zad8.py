#!/usr/bin/env python
import sys
import socket

def main():
    args = sys.argv[1:]

    if len(args) != 1:
        print("Usage: python3 zad8.py <hostname/ip>")
        sys.exit(1)

    hostname = args[0]

    for i in range(1, 65535):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((hostname, i))
            print(f"Port {i} is open, service {socket.getservbyport(i)}")
            sock.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
