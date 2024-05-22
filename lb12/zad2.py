import socket, threading
from datetime import datetime

PORT=10000

class ClientThread(threading.Thread):
    def __init__(self, conn: socket.socket, addr, log):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.log = log

    def run(self):
        while True:
            data = self.conn.recv(8192)
            self.conn.sendall(data)

            msg = f"From {self.addr}: '{data.decode()}'"
            self.log(msg)


class Server:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

        self.logfile = open("zad2_logs.txt", "a")

    def log(self, msg: str):
        msg_formatted = f"{datetime.now()}: {msg}"
        self.logfile.write(f"{msg_formatted}\n")
        self.logfile.flush()
        print(f"{msg_formatted}")

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((self.ip, self.port))
                sock.listen()

                self.log(f"Listening on {self.ip}:{self.port}")


                while True:
                    conn, addr = sock.accept()

                    self.log(f"New connection from {addr}")

                    c = ClientThread(conn, addr, self.log)
                    c.start()

        except socket.error as e:
            print(e)


if __name__ == '__main__':
    s = Server('127.0.0.1', PORT)
    s.run()
