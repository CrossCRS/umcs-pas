import socket
import struct
import time

HOST = "ntp.task.gda.pl"
PORT = 123

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(b'\x1b' + 47 * b'\0', (HOST, PORT))
    data, addr = sock.recvfrom(1024)

    sock.close()

    unpacked = struct.unpack("!12I", data)
    unpacked = unpacked[10] + unpacked[11] / 2 ** 32 - 2208988800

    print(time.ctime(unpacked))

if __name__ == "__main__":
    main()
