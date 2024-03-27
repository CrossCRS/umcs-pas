#!/usr/bin/env python3
import socket

PORT = 2915

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', PORT))

        while True:
            data, addr = sock.recvfrom(1024)

            if data.decode() == "PING":
                sock.sendto(b"PONG", addr)


if __name__ == '__main__':
    main()
