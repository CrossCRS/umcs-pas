import socket

HOST="dsmka.wintertoad.xyz"
PORT=587

LOGIN="dGVzdDFAd2ludGVydG9hZC54eXo="
PASS="UEBzc3cwcmQ="

FROM="test1@wintertoad.xyz"
TO="test2@wintertoad.xyz"
SUBJECT="HTML Test"
BODY="<b>Test</b><i>ing</i> different <u>HTML</u> tags"

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

        sock.send(b"MAIL FROM: <" + FROM.encode() + b">\r\n")
        sock.recv(1024)
        sock.send(b"RCPT TO: <" + TO.encode() + b">\r\n")
        sock.recv(1024)
        sock.send(b"DATA\r\n")
        sock.recv(1024)
        sock.send(b"Subject: " + SUBJECT.encode() + b"\r\n")
        sock.send(b"From: " + FROM.encode() + b">\r\n")
        sock.send(b"To: <" + TO.encode() + b">\r\n")

        sock.send(b"MIME-Version: 1.0\r\n")
        sock.send(b"Content-Type: multipart/mixed; boundary=sep\r\n")
        sock.send(b"--sep\r\n")
        sock.send(b"Content-Type: text/html\r\n")
        sock.send(BODY.encode() + b"\r\n")
        sock.send(b"--sep--\r\n")
        sock.send(b"\r\n.\r\n")
        print(sock.recv(1024))
    else:
        print("Login failed")

    sock.close()

if __name__ == "__main__":
    main()
