#!/usr/bin/env python3
import socket
import random

PORT = 2912

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', PORT))
        sock.listen()

        number = random.randint(0, 100)

        while True:
            conn, addr = sock.accept()

            while True:
                data = conn.recv(8192)

                try:
                    guessed = int(data.decode())
                    if guessed < number:
                        conn.send(b"TOO_SMALL")
                    elif guessed > number:
                        conn.send(b"TOO_BIG")
                    else:
                        conn.send(b"CORRECT")
                        break
                except:
                    conn.send(b"SYNTAX_ERROR")

            conn.close()
            exit(0)

if __name__ == '__main__':
    main()
