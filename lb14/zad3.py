# todo: do
import socket
import ssl

HOST="chat.freenode.net"
PORT=7000

def recv(sock):
    resp = b""
    try:
        while True:
            chunk = sock.recv(4096)
            if len(chunk) == 0:
                break
            resp += chunk
    except socket.timeout:
        pass

    if resp.decode().startswith("PING"):
        sock.send(b"PONG " + resp.split()[1] + b"\r\n")
        return recv(sock)
    
    return resp

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    sock.connect((HOST, PORT))

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock)

    print(recv(secure_sock))
    secure_sock.send(b"NICK nb_bot_4242\r\n")
    secure_sock.send(b"USER nb_bot_4242 0 * :nb_bot_4242\r\n")
    print(recv(secure_sock))

    secure_sock.send(b"VERSION\r\n")
    print(recv(secure_sock))

    secure_sock.close()

if __name__ == "__main__":
    main()
