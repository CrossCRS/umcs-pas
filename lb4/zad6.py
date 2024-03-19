#!/usr/bin/env python3
import socket

PORT = 9000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', PORT))

        while True:
            hostname, addr = sock.recvfrom(8192)

            try:
                data = socket.gethostbyaddr(hostname.decode())[2][0]
            except:
                data = 'IP not found'

            sock.sendto(data.encode(), addr)

    
if __name__ == '__main__':
    main()