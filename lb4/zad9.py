#!/usr/bin/env python3
import socket

PORT = 9000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', PORT))

        while True:
            data, addr = sock.recvfrom(8192)

            data = data.decode().split(';')
            answer = "NIE"

            if data[0] == "zad14odp" and data[1] == "src" and data[3] == "dst" and data[5] == "data":
                src = int(data[2])
                dst = int(data[4])
                data_text = data[6]

                if src == 60788 and dst == 2901 and data_text == "programming in python is fun":
                    answer = "TAK"
            else:
                answer = "BAD_SYNTAX"

            sock.sendto(answer.encode(), addr)


if __name__ == '__main__':
    main()
