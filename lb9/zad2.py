import socket

HOST="httpbin.org"
PORT=80

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((HOST, PORT))

    sock.send(f"GET /image/png HTTP/1.1\r\nHOST: {HOST}\r\nAccept: text/html,image/png\r\n\r\n".encode())
    resp = b""

    try:
        while True:
            chunk = sock.recv(4096)
            if len(chunk) == 0:
                break
            resp += chunk
    except socket.timeout:
        pass

    with open("zad2.png", "wb") as file:
        file.write(resp.split(b"\r\n\r\n")[1])

    sock.close()

if __name__ == "__main__":
    main()
