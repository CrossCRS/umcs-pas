#!/usr/bin/env python3
import socket

PORT = 9000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', PORT))

        while True:
            ip, addr = sock.recvfrom(8192)

            try:
                data = socket.gethostbyaddr(ip.decode())[0]
            except:
                data = 'Host not found'

            sock.sendto(data.encode(), addr)

    
if __name__ == '__main__':
    main()