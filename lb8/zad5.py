import socket
import re

HOST="dsmka.wintertoad.xyz"
PORT=143

LOGIN="test2@wintertoad.xyz"
PASS="P@ssw0rd"

def recv_line(sock) -> bytes:
    data = b""
    while not data.endswith(b"\r\n"):
        data += sock.recv(1)
    return data

def recv_imap(sock) -> list[bytes]:
    lines = []
    while True:
        line = recv_line(sock)
        lines.append(line)

        if not line.startswith(b"*"):
            break

    return lines

TAG_COUNTER = 0
def send_imap(sock, msg, getall=False) -> list[bytes]:
    global TAG_COUNTER

    sock.send(f"A{TAG_COUNTER} {msg}\r\n".encode())
    TAG_COUNTER += 1

    if getall:
        return sock.recv(8192)

    return recv_imap(sock)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    sock.recv(4096)
    send_imap(sock, f"LOGIN {LOGIN} {PASS}")
    response = send_imap(sock, "SELECT INBOX")

    if response[1].find(b"OK") == -1:
        sock.close()
        exit(-1)

    response = send_imap(sock, "STORE 1 +FLAGS \Deleted")

    if response[-1].find(b"OK") == -1:
        sock.close()
        exit(-1)

    response = send_imap(sock, "EXPUNGE")

    if response[-1].find(b"OK") == -1:
        sock.close()
        exit(-1)

    print("Message deleted")

    sock.close()

if __name__ == "__main__":
    main()
