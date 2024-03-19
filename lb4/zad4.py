#!/usr/bin/env python3
import socket

PORT = 9000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', PORT))

        while True:
            a, addr = sock.recvfrom(8192)
            op, addr = sock.recvfrom(8192)
            b, addr = sock.recvfrom(8192)

            op = op.decode()
            a = int(a.decode())
            b = int(b.decode())

            if op == '+':
                data = a + b
            elif op == '-':
                data = a - b
            elif op == '*':
                data = a * b
            elif op == '/':
                data = a / b
            else:
                data = 'Invalid operator'

            sock.sendto(str(data).encode(), addr)

    
if __name__ == '__main__':
    main()