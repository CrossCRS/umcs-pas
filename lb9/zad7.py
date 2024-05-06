#!/usr/bin/env python3
import socket

PORT = 1234

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', PORT))
        sock.listen()

        while True:
            conn, addr = sock.accept()

            data = conn.recv(8192)
            print(data)

            response = "<h1>Test xd</h1>"

            sock.sendall(f"HTTP/1.1 200 OK\r\nServer: DSMka\r\nContent-Type: text/html\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode())

            conn.close()

if __name__ == '__main__':
    main()
