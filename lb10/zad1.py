import socket
import random
import base64

HOST="localhost"
PORT=10000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((HOST, PORT))

    key = random.randbytes(16).hex()
    key = base64.b64encode(key.encode()).decode()

    sock.send(f"GET ws://{HOST}:{PORT}/ HTTP/1.1\r\nHOST: {HOST}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
    resp = b""

    try:
        while True:
            chunk = sock.recv(4096)
            if len(chunk) == 0:
                break
            resp += chunk
    except socket.timeout:
        pass

    print(resp.decode(errors='ignore').split("\r\n")[0])

    sock.close()

if __name__ == "__main__":
    main()
