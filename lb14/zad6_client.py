import socket
import ssl

HOST="localhost"
PORT=10000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.load_verify_locations('server.pem')
    context.load_cert_chain('client.pem', 'client_key.pem')

    secure_sock = context.wrap_socket(sock)
    secure_sock.settimeout(3)
    secure_sock.connect((HOST, PORT))

    while True:
        msg = input("Enter message: ")

        secure_sock.sendall(msg.encode())
        print(secure_sock.recv(8192).decode())

    secure_sock.close()

if __name__ == "__main__":
    main()
