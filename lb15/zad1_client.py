import socket
import ssl

HOST="localhost"
PORT=10000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((HOST, PORT))

    while True:
        msg = input("Enter message: ")

        sock.sendall(msg.encode())
        print(sock.recv(8192).decode())

    sock.close()

if __name__ == "__main__":
    main()
