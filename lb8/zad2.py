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
def send_imap(sock, msg) -> list[bytes]:
    global TAG_COUNTER

    sock.send(f"A{TAG_COUNTER} {msg}\r\n".encode())
    TAG_COUNTER += 1
    return recv_imap(sock)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    sock.recv(4096)
    send_imap(sock, f"LOGIN {LOGIN} {PASS}")
    response = send_imap(sock, "STATUS INBOX (MESSAGES)")

    if response[-1].find(b"OK") == -1:
        sock.close()
        exit(-1)

    msg_count = re.findall(r"\(MESSAGES (\d+)\)", response[0].decode())
    print(msg_count[0])

    sock.close()

if __name__ == "__main__":
    main()
