#!/usr/bin/env python3
import socket

PORT = 9000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', PORT))

        while True:
            data, addr = sock.recvfrom(8192)
            sock.sendto(data, addr)

    
if __name__ == '__main__':
    main()