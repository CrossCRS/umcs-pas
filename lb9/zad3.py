import socket

HOST="httpbin.org" # Nie obsluguje naglowka Range?
PORT=80

def main():
    for i in range(3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((HOST, PORT))

        if i == 2:
            content_range = f"bytes={i*3072}-"
        else:
            content_range = f"bytes={i*3072}-{(i+1)*3072-1}"

        sock.send(f"GET /image/png HTTP/1.1\r\nHOST: {HOST}\r\nAccept: text/html,image/png\r\nRange: {content_range}\r\n\r\n".encode())
        resp = b""

        try:
            while True:
                chunk = sock.recv(4096)
                if len(chunk) == 0:
                    break
                resp += chunk
        except socket.timeout:
            pass

        with open(f"zad3.png.chunk{i}", "wb") as file:
            file.write(resp.split(b"\r\n\r\n")[1])

        sock.close()

    for i in range(3):
        with open(f"zad3.png.chunk{i}", "rb") as file:
            chunk = file.read()
            with open("zad3.png", "ab") as f:
                f.write(chunk)

if __name__ == "__main__":
    main()
