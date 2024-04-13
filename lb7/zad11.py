import socket

HOST="dsmka.wintertoad.xyz"
PORT=110

LOGIN="test2@wintertoad.xyz"
PASS="P@ssw0rd"

MAIL_ID=11

def recv_all_until(sockfd, crlf):
    data = b""
    while not data.endswith(crlf):
        data = data + sockfd.recv(1)
    return data

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

        sock.send(b"RETR " + str(MAIL_ID).encode() + b"\r\n")

        resp = recv_all_until(sock, b".\r\n").decode()
        print(resp)
    else:
        print("Login failed")

    sock.close()

if __name__ == "__main__":
    main()
