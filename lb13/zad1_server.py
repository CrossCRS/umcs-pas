import socket, threading

PORT=10000

class ClientThread(threading.Thread):
    def __init__(self, conn: socket.socket):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        while True:
            data = self.conn.recv(8192)
            data_decoded = data.decode(errors='ignore')
            data_split = data_decoded.split('\x1f')

            if data_split[0] == "PUT":
                try:
                    f = open(f"zad1/received/{data_split[1]}", "wb")
                    size = int(data_split[2])
                    self.conn.sendall("READY\r\n".encode())

                    received = 0
                    while received < size:
                        data = self.conn.recv(8192)
                        f.write(data)
                        received += len(data)

                    f.close()
                    self.conn.sendall("OK\r\n".encode())
                except:
                    self.conn.sendall("ERROR\r\n".encode())
            elif data_decoded == "EXIT\r\n":
                self.conn.close()
                break
            else:
                self.conn.sendall("INVALID_CMD\r\n".encode())


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
