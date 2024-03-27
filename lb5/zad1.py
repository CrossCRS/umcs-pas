import socket

HOST = "127.0.0.1" #"212.182.24.27"
PORT = 2912

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    while True:
        number = input("Guess a number [0-100]: ")
        sock.send(str(number).encode())
        data = sock.recv(1024).decode()

        print(data + "\n")

        if data == "CORRECT":
            break

    sock.close()

if __name__ == "__main__":
    main()
