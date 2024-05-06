#!/usr/bin/env python3
import socket

PORT = 1234

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', PORT))
        sock.listen()

        response_404 = None

        with open("examples/404.html", "r") as f:
            response = f.read()
            response_404 = f"HTTP/1.1 404 Not Found\r\nServer: DSMka\r\nContent-Type: text/html\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode()

        while True:
            conn, addr = sock.accept()

            data = conn.recv(8192).decode()
            lines = data.split("\r\n")

            print(f"{addr[0]}: {lines[0]}")

            if lines[0].split(" ")[0] != "GET":
                conn.sendall("HTTP/1.1 405 Method Not Allowed\r\nServer: DSMka\r\n\r\n".encode())
                conn.close()
                continue
                
            file = lines[0].split(" ")[1]

            if file == "/":
                file = "/index.html"

            response = None

            try:
                with open(f"examples{file}", "r") as f:
                    response = f.read()
            except FileNotFoundError:
                conn.sendall(response_404)
                conn.close()
                continue

            conn.sendall(f"HTTP/1.1 200 OK\r\nServer: DSMka\r\nContent-Type: text/html\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode())

            conn.close()

if __name__ == '__main__':
    main()
