import socket

HOST="localhost"
PORT=10000

FILE="diagram.jpg"

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((HOST, PORT))

    data = None
    with open(f"zad1/{FILE}", "rb") as f:
        data = f.read()

    if data is None:
        print("Error: Couldn't read file")
        return

    sock.sendall(f"PUT\x1f{FILE}\x1f{len(data)}\r\n".encode())

    resp = sock.recv(8192)

    if resp.decode() != "READY\r\n":
        print("Error: Server not ready")
        return
    
    sock.sendall(data)

    print(sock.recv(8192).decode())

    sock.sendall("EXIT\r\n".encode())

    sock.close()

if __name__ == "__main__":
    main()
