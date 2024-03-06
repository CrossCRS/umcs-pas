import socket

HOST = "127.0.0.1" #"212.182.24.27"
PORT = 2900

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    while sock:
        msg = input("Enter message: ")
        sock.send(msg.encode())
        data = sock.recv(1024)
        print(data)

    sock.close()

if __name__ == "__main__":
    main()
