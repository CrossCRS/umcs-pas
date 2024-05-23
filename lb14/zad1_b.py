import socket
import ssl

HOST="dsmka.wintertoad.xyz"
PORT=465

LOGIN="dGVzdDFAd2ludGVydG9hZC54eXo="
PASS="UEBzc3cwcmQ="

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('./examples/GeoTrustGlobalCA.pem')
    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock)

    cert = secure_sock.getpeercert()
    if not cert:
        raise Exception('Certificate error')

    secure_sock.recv(1024)
    secure_sock.send(b"EHLO test1\r\n")
    secure_sock.recv(1024)
    secure_sock.send(b"AUTH LOGIN\r\n")
    secure_sock.recv(1024)
    secure_sock.send((LOGIN + "\r\n").encode())
    secure_sock.recv(1024)
    secure_sock.send((PASS + "\r\n").encode())
    resp = secure_sock.recv(1024)

    print(resp)

    if resp.decode() == "235 2.7.0 Authentication successful\r\n":
        print("Logged in")

        subject = input("Subject: ")
        recipients = []

        recp = "."
        while recp != "":
            recp = input("Recipient (empty to end adding): ")
            if recp != "":
                recipients.append(recp)

        email_from = input("From: ")
        email_body = input("Body: ")

        secure_sock.send(b"MAIL FROM: <" + email_from.encode() + b">\r\n")
        secure_sock.recv(1024)
        for recp in recipients:
            secure_sock.send(b"RCPT TO: <" + recp.encode() + b">\r\n")
            secure_sock.recv(1024)

        secure_sock.send(b"DATA\r\n")
        secure_sock.recv(1024)
        secure_sock.send(b"Subject: " + subject.encode() + b"\r\n")
        secure_sock.send(b"From: " + email_from.encode() + b">\r\n")
        secure_sock.send(b"To: <" + recipients[0].encode() + b">\r\n")
        if len(recipients) > 1:
            secure_sock.send(b"CC: <" + ",".join(recipients[1:]).encode() + b">\r\n")

        secure_sock.send(b"\r\n")
        secure_sock.send(email_body.encode())
        secure_sock.send(b"\r\n.\r\n")
        print(secure_sock.recv(1024))
    else:
        print("Login failed")

    secure_sock.close()

if __name__ == "__main__":
    main()
