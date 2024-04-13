# TODO: Naprawic
#!/usr/bin/env python3
import socket
import random

PORT = 1234

EHLO_RESPONSE = "250-mail.example.com\r\n250-PIPELINING\r\n250-SIZE 10240000\r\n250-ETRN\r\n250-AUTH PLAIN LOGIN\r\n250-AUTH=PLAIN LOGIN\r\n250-ENHANCEDSTATUSCODES\r\n250-8BITMIME\r\n250-DSN\r\n250 CHUNKING\r\n"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', PORT))
        sock.listen()

        while True:
            conn, addr = sock.accept()

            conn.send(b"220 mail.example.com ESMTP\r\n")

            authenticated = False
            auth_mode = False
            auth_state = -1
            data_mode = False

            while True:
                data = conn.recv(4096).decode()
                data_split = data.split(" ")

                if data_split[0].upper() == "QUIT\r\n":
                    break
                elif data.upper() == "AUTH LOGIN\r\n" and auth_state == 0:
                    conn.send(b"334 VXNlcm5hbWU6\r\n")
                    auth_state = 1
                elif data_split[0].upper() == "HELO" and len(data_split) == 2:
                    authenticated = True
                    conn.send(b"250 mail.example.com OK\r\n")
                elif data_split[0].upper() == "EHLO":
                    authenticated = False
                    auth_mode = True
                    auth_state = 0
                    conn.send(EHLO_RESPONSE.encode())
                elif data_split[0].upper() == "MAIL" and len(data_split) > 2:
                    if not authenticated:
                        conn.send(b"503 5.5.1 Error: send HELO/EHLO first\r\n")
                        break
                    if data_split[1].upper() == "FROM:":
                        pass
                    elif data_split[1].upper() == "TO:":
                        pass
                    else:
                        conn.send(b"501 Syntax\r\n")
                elif data_split[0].upper() == "DATA":
                    if not authenticated:
                        conn.send(b"503 5.5.1 Error: send HELO/EHLO first\r\n")
                        break
                    data_mode = True
                    conn.send(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                elif data == "\r\n.\r\n" and data_mode:
                    if not authenticated:
                        conn.send(b"503 5.5.1 Error: send HELO/EHLO first\r\n")
                        break
                    data_mode = False
                    conn.send(b"250 OK\r\n")
                else:
                    if auth_mode and auth_state != 3:
                        if auth_state == 1:
                            conn.send(b"334 UGFzc3dvcmQ6\r\n")
                            auth_state = 2
                        elif auth_state == 2:
                            conn.send(b"235 2.7.0 Authentication successful\r\n")
                            auth_state = 3
                            authenticated = True
                            auth_mode = False

                    if not data_mode:
                        conn.send(b"501 Syntax\r\n")

            conn.close()

if __name__ == '__main__':
    main()
