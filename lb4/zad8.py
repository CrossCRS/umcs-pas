#!/usr/bin/env python3
import socket

PORT = 9000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', PORT))
        sock.listen()

        while True:
            conn, addr = sock.accept()

            data = b""
            while len(data) < 20:
                data += conn.recv(20)

            conn.send(data)
            conn.close()


if __name__ == '__main__':
    main()