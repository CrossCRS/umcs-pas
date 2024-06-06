import socket
import ssl

HOST="localhost"
PORT=10000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((HOST, PORT))

    sock.sendall("WEATHER\r\n".encode())
    data = sock.recv(8192).decode()

    print(data)

    sock.close()

if __name__ == "__main__":
    main()
