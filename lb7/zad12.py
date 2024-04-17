#!/usr/bin/env python3
import socket

PORT = 1234

def main():
    example_mail = None
    example_mail_size = None

    with open("example_mail.txt", "r") as f:
        example_mail = f.read()
        example_mail_size = len(example_mail)

    mails = []
    for i in range(10):
        mails.append({ "data": example_mail, "size": example_mail_size })

    if example_mail == None or example_mail_size == None:
        print("Failed to read example_mail.txt")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', PORT))
        sock.listen()

        while True:
            conn, addr = sock.accept()

            conn.send(b"+OK Dovecot (Debian) ready.\r\n")

            authenticated = False
            user = None

            while True:
                data = conn.recv(4096)
                
                if not data:
                    continue

                data = data.decode('utf-8', 'ignore')
                data_split = data.replace("\r\n", "").split(" ")

                if data_split[0].upper() == "QUIT":
                    conn.send(b"+OK Logging out\r\n")
                    break
                elif data_split[0].upper() == "USER" and len(data_split) == 2 and authenticated == False:
                    user = data_split[1]
                    conn.send(b"+OK\r\n")
                elif data_split[0].upper() == "PASS" and len(data_split) == 2 and user and authenticated == False:
                    authenticated = True
                    conn.send(b"+OK Logged in.\r\n")
                elif data_split[0].upper() == "STAT" and authenticated == True:
                    size = 0
                    for mail in mails:
                        size += mail["size"]
                    conn.send(f"+OK {len(mails)} {size}\r\n".encode())
                elif data_split[0].upper() == "LIST" and authenticated == True:
                    conn.send(f"+OK {len(mails)} messages\r\n".encode())
                    for i, mail in enumerate(mails):
                        conn.send(f"{i+1} {mail['size']}\r\n".encode())
                    conn.send(b".\r\n")
                elif data_split[0].upper() == "RETR" and len(data_split) == 2 and authenticated == True:
                    mail_id = int(data_split[1])
                    if mail_id > 0 and mail_id <= len(mails):
                        conn.send(f"+OK {mails[mail_id-1]['size']} octets\r\n".encode())
                        conn.send(mails[mail_id-1]["data"].encode())
                        conn.send(b"\r\n.\r\n")
                    else:
                        conn.send(f"-ERR There's no message {mail_id}.\r\n".encode())
                elif data_split[0].upper() == "DELE" and len(data_split) == 2 and authenticated == True:
                    mail_id = int(data_split[1])
                    if mail_id > 0 and mail_id <= len(mails):
                        mails.pop(mail_id-1)
                        conn.send(b"+OK Message deleted.\r\n")
                    else:
                        conn.send(f"-ERR There's no message {mail_id}.\r\n".encode())
                else:
                    conn.send(b"-ERR Unknown command.\r\n")

            conn.close()

if __name__ == '__main__':
    main()
