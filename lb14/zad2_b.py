import socket
import ssl

HOST="httpbin.org"
PORT=443

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((HOST, PORT))

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('./examples/GeoTrustGlobalCA.pem')

    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock)

    cert = secure_sock.getpeercert()
    if not cert:
        raise Exception('Certificate error')

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

    with open("zad2_b.html", "wb") as file:
        file.write(resp.split(b"\r\n\r\n")[1])

    secure_sock.close()

if __name__ == "__main__":
    main()
