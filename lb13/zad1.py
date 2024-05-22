import socket, threading, os

PORT=10000

class ClientThread(threading.Thread):
    def __init__(self, conn: socket.socket):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        while True:
            data = self.conn.recv(8192)
            data_decoded = data.decode(errors='ignore')
            data_split = data_decoded.split(' ')

            if data_decoded == "LIST\r\n":
                files = next(os.walk('files/'))[2]
                msg = ""
                for f in files:
                    msg += f"'{f}'"
                    msg += " "
                
                self.conn.sendall(f"{msg}\r\n".encode())
            elif data_split[0] == "GET":
                try:
                    f = open(f"files/{data_split[1:]}", "rb")
                    f_data = f.read()
                    # TODO: Send xd
                except:
                    self.conn.sendall("INVALID_FILE\r\n".encode())
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
