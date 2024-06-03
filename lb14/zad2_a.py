import socket
import ssl

HOST="httpbin.org"
PORT=443

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((HOST, PORT))

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock)

    secure_sock.send(f"GET /html HTTP/1.1\r\nHOST: {HOST}\r\nUser-Agent: Safari 7.0.3\r\n\r\n".encode())
    resp = b""

    try:
        while True:
            chunk = secure_sock.recv(4096)
            if len(chunk) == 0:
                break
            resp += chunk
    except socket.timeout:
        pass

    with open("zad2_a.html", "wb") as file:
        file.write(resp.split(b"\r\n\r\n")[1])

    secure_sock.close()

if __name__ == "__main__":
    main()
