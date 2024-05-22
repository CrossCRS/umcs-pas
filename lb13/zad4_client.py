import socket
import re

HOST="localhost"
PORT=10000

def recv_all_until(sockfd, crlf):
    data = b""
    while not data.endswith(crlf):
        data = data + sockfd.recv(1)
    return data

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((HOST, PORT))

    sock.sendall("LIST\r\n".encode())

    resp = recv_all_until(sock, b"\r\n")

    print("Available files: " + resp.decode().strip())

    requested_file = input("Enter file name: ")

    sock.sendall(f"GET_IMAGE {requested_file}\r\n".encode())

    resp = recv_all_until(sock, b"\r\n")

    m = re.match(r"SIZE (\d+) NAME (.*)\r\n", resp.decode())
    
    if m is None:
        print("Error: Invalid response")
        return
    
    size = int(m.group(1))
    file = m.group(2)

    print(f"Receiving file '{file}' with size of {size} bytes")

    with open(f"zad4/received/{file}", "wb") as f:
        received = 0
        while received < size:
            data = sock.recv(8192)
            f.write(data)
            received += len(data)

    sock.close()

if __name__ == "__main__":
    main()
