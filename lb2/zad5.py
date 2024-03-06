import socket

HOST = "127.0.0.1" #"212.182.24.27"
PORT = 2901

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        msg = input("Enter message: ")
        sock.sendto(msg.encode(), (HOST, PORT))
        data = sock.recv(1024)
        print(data)

    sock.close()

if __name__ == "__main__":
    main()
