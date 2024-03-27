#!/usr/bin/env python3
import socket
import random

PORT = 2914

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', PORT))
        sock.listen()

        while True:
            conn, addr = sock.accept()

            data = conn.recv(1024)
            if data.decode() == "PING":
                conn.send(b"PONG")

            conn.close()

if __name__ == '__main__':
    main()
