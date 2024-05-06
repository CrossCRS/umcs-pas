import socket
import random
import base64

HOST="localhost"
PORT=10000

def xor(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

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

    frame = bytearray()
    frame.append(int('10000001', 2)) # FIN[0], RSV1[1], RSV2[2], RSV3[3], opcode[4-7] (1 = text)
    frame.append(int('10000110', 2)) # MASK[0], dlugosc[1-7] (= 6)
    masking_key = random.randbytes(4)
    frame += masking_key

    payload = xor(b"Hello!", masking_key)
    frame += payload

    sock.sendall(frame)

    print("Received: " + sock.recv(4096).decode(errors='ignore'))

    sock.close()

if __name__ == "__main__":
    main()
