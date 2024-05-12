#!/usr/bin/env python3
import base64
import hashlib
import socket
import re

PORT = 10000

def xor(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def sha1(text):
    hash_object = hashlib.sha1(text.encode())
    return hash_object.hexdigest()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', PORT))
        sock.listen()

        while True:
            conn, addr = sock.accept()

            data = conn.recv(8192).decode()
            lines = data.split("\r\n")

            if lines[0].split(" ")[0] != "GET":
                conn.sendall("HTTP/1.1 405 Method Not Allowed\r\nServer: DSMka\r\n\r\n".encode())
                conn.close()
                continue
                
            if "upgrade: websocket" in data.lower():
                client_key = re.findall(r"Sec-WebSocket-Key: (.+)", data)[0]
                server_key = base64.b64encode(sha1(client_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).decode()

                conn.sendall(f"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: {server_key}\r\n\r\n".encode())

                while True:
                    data = conn.recv(8192)

                    fin = data[0] & 0b10000000
                    opcode = data[0] & 0b00001111
                    mask = data[1] & 0b10000000
                    length = data[1] & 0b01111111

                    if fin == 0:
                        break
                    if opcode != 1:
                        break
                    if mask == 0:
                        break

                    mask_offset = 2
                    if length == 126:
                        length = int.from_bytes(data[2:4], 'big')
                        mask_offset = 4
                    elif length == 127:
                        length = int.from_bytes(data[2:10], 'big')
                        mask_offset = 10

                    masking_key = data[mask_offset:mask_offset+4]
                    payload = xor(data[mask_offset+4:], masking_key)

                    print(payload.decode())

                    # Odpowiedź
                    frame = bytearray()
                    frame.append(int('10000001', 2)) # FIN[0], RSV1[1], RSV2[2], RSV3[3], opcode[4-7] (1 = text)
                    
                    if len(payload) <= 125:
                        frame.append(len(payload))
                    elif len(payload) <= 65535: # 16 bit
                        frame.append(int('01111110', 2))
                        frame += len(payload).to_bytes(2, 'big')
                    else: # 64 bit
                        frame.append(int('01111111', 2))
                        frame += len(payload).to_bytes(8, 'big')
                    
                    for i in range(4):
                        frame.append(int('00000000', 2))

                    frame += payload

                    conn.sendall(frame)
    
                
                conn.close()
                continue

            conn.sendall("HTTP/1.1 405 Method Not Allowed\r\nServer: DSMka\r\n\r\n".encode())
            conn.close()

if __name__ == '__main__':
    main()
