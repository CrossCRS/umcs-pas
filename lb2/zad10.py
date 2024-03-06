import socket

HOST = "127.0.0.1" #"212.182.24.27"
PORT = 2907

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto("google.com".encode(), (HOST, PORT))

    data = sock.recv(1024).decode()
    print(data)

    sock.close()

if __name__ == "__main__":
    main()
