import socket

HOST="dsmka.wintertoad.xyz"
PORT=110

LOGIN="test2@wintertoad.xyz"
PASS="P@ssw0rd"

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    sock.recv(1024)
    sock.send(b"USER " + LOGIN.encode() + b"\r\n")
    sock.recv(1024)
    sock.send(b"PASS " + PASS.encode() + b"\r\n")
    resp = sock.recv(1024)

    if resp.decode() == "+OK Logged in.\r\n":
        print("Logged in")

        sock.send(b"STAT\r\n")

        resp = sock.recv(1024)
        print("Message count: " + resp.decode().split(" ")[1])
    else:
        print("Login failed")

    sock.close()

if __name__ == "__main__":
    main()
