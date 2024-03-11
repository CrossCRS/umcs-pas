#!/usr/bin/env python3
import socket

def parse_udp(data):
    src_port = int(data[0] << 8) + int(data[1])
    dst_port = int(data[2] << 8) + int(data[3])
    data_length = int(data[4] << 8) + int(data[5])
    data_str = data[8:data_length]

    data_str = ''.join([chr(x) for x in data_str])

    return src_port, dst_port, data_str

def main():
    data = [0xed, 0x74, 0x0b, 0x55, 0x00, 0x24, 0xef, 0xfd, 0x70, 0x72, 0x6f, 0x67, 0x72, 0x61, 0x6d, 0x6d, 0x69, 0x6e, 0x67, 0x20, 0x69, 0x6e, 0x20, 0x70, 0x79, 0x74, 0x68, 0x6f, 0x6e, 0x20, 0x69, 0x73, 0x20, 0x66, 0x75, 0x6e]

    src_port, dst_port, data_str = parse_udp(data)

    msg = f"zad14odp;src;{src_port};dst;{dst_port};data;{data_str}"
    print(msg)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), ('127.0.0.1', 2910))
    print(sock.recv(1024))

if __name__ == "__main__":
    main()
