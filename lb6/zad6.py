import socket

HOST="dsmka.wintertoad.xyz"
PORT=587

LOGIN="dGVzdDFAd2ludGVydG9hZC54eXo="
PASS="UEBzc3cwcmQ="

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    sock.recv(1024)
    sock.send(b"EHLO test1\r\n")
    sock.recv(1024)
    sock.send(b"AUTH LOGIN\r\n")
    sock.recv(1024)
    sock.send((LOGIN + "\r\n").encode())
    sock.recv(1024)
    sock.send((PASS + "\r\n").encode())
    resp = sock.recv(1024)

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

        sock.send(b"MAIL FROM: <" + email_from.encode() + b">\r\n")
        sock.recv(1024)
        for recp in recipients:
            sock.send(b"RCPT TO: <" + recp.encode() + b">\r\n")
            sock.recv(1024)

        sock.send(b"DATA\r\n")
        sock.recv(1024)
        sock.send(b"Subject: " + subject.encode() + b"\r\n")
        sock.send(b"From: " + email_from.encode() + b"\r\n")
        sock.send(b"To: <" + recipients[0].encode() + b">\r\n")
        if len(recipients) > 1:
            sock.send(b"CC: <" + ",".join(recipients[1:]).encode() + b">\r\n")

        sock.send(b"\r\n")
        sock.send(email_body.encode())
        sock.send(b"\r\n.\r\n")
        print(sock.recv(1024))
    else:
        print("Login failed")

    sock.close()
    pass

if __name__ == "__main__":
    main()
