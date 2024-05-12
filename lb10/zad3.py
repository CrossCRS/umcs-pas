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

    message = input("Enter message to send: ")
    message_length = len(message)

    frame = bytearray()
    frame.append(int('10000001', 2)) # FIN[0], RSV1[1], RSV2[2], RSV3[3], opcode[4-7] (1 = text)
    
    if message_length <= 125:
        frame.append(int('10000000', 2) | message_length) # MASK[0], dlugosc[1-7]
    elif message_length <= 65535: # 16 bit
        frame.append(int('11111110', 2)) # MASK[0], dlugosc[1-7] = 126
        frame += message_length.to_bytes(2, 'big')
    else: # 64 bit
        frame.append(int('11111111', 2)) # MASK[0], dlugosc[1-7] = 127
        frame += message_length.to_bytes(8, 'big')
    masking_key = random.randbytes(4)
    frame += masking_key

    payload = xor(message.encode(), masking_key)
    frame += payload

    sock.sendall(frame)

    data = sock.recv(8192)
    payload_length = data[1] & 0b01111111

    if payload_length == 126:
        payload_length = int.from_bytes(data[2:4], 'big')
    elif payload_length == 127:
        payload_length = int.from_bytes(data[2:10], 'big')
    
    payload = data[-payload_length:]

    print("Received: " + payload.decode(errors='ignore'))

    sock.close()

if __name__ == "__main__":
    main()
