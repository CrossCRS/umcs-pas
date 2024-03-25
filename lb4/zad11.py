#!/usr/bin/env python3
import socket

PORT = 2911

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', PORT))

        while True:
            data, addr = sock.recvfrom(8192)

            data = data.decode().split(';')
            answer = "NIE"

            if data[0] == "zad15odpA":
                ver = int(data[2])
                srcip = data[4]
                dstip = data[6]
                type = int(data[8])

                if ver == 4 and srcip == "212.182.24.27" and dstip == "192.168.0.2" and type == 6:
                    answer = "TAK"
            elif data[0] == "zad15odpB":
                srcport = int(data[2])
                dstport = int(data[4])
                data = data[6]

                if srcport == 2900 and dstport == 47526 and data == "network programming is fun":
                    answer = "TAK"
            else:
                answer = "BAD_SYNTAX"

            sock.sendto(answer.encode(), addr)


if __name__ == '__main__':
    main()
