import socket, threading

PORT=10000

class ClientThread(threading.Thread):
    def __init__(self, conn: socket.socket):
        threading.Thread.__init__(self)
        self.conn = conn

        self.data = None
        with open("zad3/diagram.jpg", "rb") as f:
            self.data = f.read()

        if self.data is None:
            print("Error: Couldn't read zad3/diagram.jpg")
            return

    def run(self):
        while True:
            data = self.conn.recv(8192)
            data_decoded = data.decode(errors='ignore')

            if data_decoded == "GET_IMAGE\r\n":
                self.conn.sendall(f"SIZE {len(self.data)} NAME diagram.jpg\r\n".encode())
                self.conn.sendall(self.data)
            else:
                self.conn.sendall("ERROR\r\n".encode())


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
