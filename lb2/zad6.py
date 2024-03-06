import socket

HOST = "127.0.0.1" #"212.182.24.27"
PORT = 2902

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    num1 = input("Enter first number: ")
    operator = input("Enter operator: ")
    num2 = input("Enter second number: ")

    sock.sendto(num1.encode(), (HOST, PORT))
    sock.sendto(operator.encode(), (HOST, PORT))
    sock.sendto(num2.encode(), (HOST, PORT))

    data = sock.recv(1024).decode()
    print(data)

    sock.close()

if __name__ == "__main__":
    main()
