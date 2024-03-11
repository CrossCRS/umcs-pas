#!/usr/bin/env python3
import socket

def parse_tcp(data):
    src_port = int(data[0] << 8) + int(data[1])
    dst_port = int(data[2] << 8) + int(data[3])
    data_str = data[32:]

    data_str = ''.join([chr(x) for x in data_str])

    return src_port, dst_port, data_str

def main():
    data = [0x0b, 0x54, 0x89, 0x8b, 0x1f, 0x9a, 0x18, 0xec, 0xbb, 0xb1, 0x64, 0xf2, 0x80, 0x18, 0x00, 0xe3, 0x67, 0x71, 0x00, 0x00, 0x01, 0x01, 0x08, 0x0a, 0x02, 0xc1, 0xa4, 0xee, 0x00, 0x1a, 0x4c, 0xee, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x3a, 0x29]

    src_port, dst_port, data_str = parse_tcp(data)

    msg = f"zad13odp;src;{src_port};dst;{dst_port};data;{data_str}"
    print(msg)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), ('127.0.0.1', 2909))
    print(sock.recv(1024))

if __name__ == "__main__":
    main()
