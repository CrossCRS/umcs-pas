import socket, threading
import random

PORT=10000

class ClientThread(threading.Thread):
    def __init__(self, conn: socket.socket):
        threading.Thread.__init__(self)
        self.conn = conn
        self.number = random.randint(0, 100)

    def run(self):
        while True:
            data = self.conn.recv(8192)
            try:
                guess = int(data.decode())

                if guess < self.number:
                    self.conn.sendall("NUMBER_TOO_SMALL\n".encode())
                elif guess > self.number:
                    self.conn.sendall("NUMBER_TOO_BIG\n".encode())
                else:
                    self.conn.sendall("NUMBER_CORRECT\n".encode())
                    self.conn.close()
                    break
            except:
                self.conn.sendall("NUMBER_INVALID\n".encode())


class Server:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((self.ip, self.port))
                sock.listen()

                print(f"Listening on {self.ip}:{self.port}")

                while True:
                    conn, addr = sock.accept()

                    print(f"New connection from {addr}")

                    c = ClientThread(conn)
                    c.start()

        except socket.error as e:
            print(e)


if __name__ == '__main__':
    s = Server('127.0.0.1', PORT)
    s.run()
