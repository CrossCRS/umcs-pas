import socket, threading, ssl

PORT=10000

class ClientThread(threading.Thread):
    def __init__(self, conn: socket.socket):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        while True:
            data = self.conn.recv(8192)
            self.conn.sendall(data)


class Server:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_cert_chain('server.pem', 'server_key.pem') # Cert key password: P@ssw0rd
                context.verify_mode = ssl.CERT_REQUIRED
                context.load_verify_locations('client.pem')

                secure_sock = context.wrap_socket(sock, server_side=True)
                secure_sock.bind((self.ip, self.port))
                secure_sock.listen()

                print(f"Listening on {self.ip}:{self.port}")

                while True:
                    try:
                        conn, addr = secure_sock.accept()

                        print(f"New connection from {addr}")

                        c = ClientThread(conn)
                        c.start()
                    except ssl.SSLError as e:
                        print(e)

        except socket.error as e:
            print(e)


if __name__ == '__main__':
    s = Server('127.0.0.1', PORT)
    s.run()
