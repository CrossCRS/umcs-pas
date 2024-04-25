#!/usr/bin/env python3
import socket

PORT = 1234

def main():
    example_mail = None

    with open("example_mail.txt", "r") as f:
        example_mail = f.read()

    if example_mail == None:
        print("Failed to read example_mail.txt")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', PORT))
        sock.listen()

        while True:
            conn, addr = sock.accept()

            conn.send(b"* OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ AUTH=PLAIN AUTH=LOGIN] Dovecot (Debian) ready.\r\n")

            authenticated = False
            selected_mailbox = None

            while True:
                data = conn.recv(4096)

                if not data:
                    continue

                data = data.decode('utf-8', 'ignore')
                data_split = data.replace("\r\n", "").split(" ")

                if data_split[1].upper() == "LOGIN" and len(data_split) >= 4:
                    authenticated = True
                    conn.send(data_split[0].encode() + b" OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES THREAD=REFS THREAD=ORDEREDSUBJECT MULTIAPPEND URL-PARTIAL CATENATE UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS BINARY MOVE SNIPPET=FUZZY PREVIEW=FUZZY STATUS=SIZE SAVEDATE LITERAL+ NOTIFY SPECIAL-USE QUOTA] Logged in\r\n")
                elif data_split[1].upper() == "LIST" and authenticated:
                    conn.send(b"* LIST (\HasNoChildren) \".\" INBOX\r\n")
                    conn.send(data_split[0].encode() + b" OK List completed (0.000 + 0.000 + 0.000 secs).\r\n")
                elif data_split[1].upper() == "STATUS" and authenticated:
                    if data_split[2].upper() == "INBOX":
                        conn.send(b"* STATUS INBOX (MESSAGES 1)\r\n")
                        conn.send(data_split[0].encode() + b" OK Status completed (0.000 + 0.000 secs).\r\n")
                    else:
                        conn.send(data_split[0].encode() + b" NO Mailbox doesn't exist: " + data_split[2].encode() + b" (0.000 + 0.000 + 0.000 secs).\r\n")
                elif data_split[1].upper() == "SELECT" and authenticated and len(data_split) >= 3:
                    if data_split[2].upper() == "INBOX":
                        selected_mailbox = "INBOX"
                        conn.send(b"* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)\r\n")
                        conn.send(b"* OK [PERMANENTFLAGS (\Answered \Flagged \Deleted \Seen \Draft \*)] Flags permitted.\r\n")
                        conn.send(b"* 1 EXISTS\r\n")
                        conn.send(b"* 0 RECENT\r\n")
                        conn.send(b"* OK [UNSEEN 1] First unseen.\r\n")
                        conn.send(b"* OK [UIDVALIDITY 1712573141] UIDs valid\r\n")
                        conn.send(b"* OK [UIDNEXT 2] Predicted next UID\r\n")
                        conn.send(f"{data_split[0]} OK [READ-WRITE] Select completed (0.000 + 0.000 secs).\r\n".encode())
                    else:
                        conn.send(data_split[0].encode() + b" NO Mailbox doesn't exist: " + data_split[2].encode() + b" (0.000 + 0.000 + 0.000 secs).\r\n")
                elif data_split[1].upper() == "FETCH" and authenticated:
                    if selected_mailbox == None:
                        conn.send(data_split[0].encode() + b" BAD No mailbox selected (0.000 + 0.000 secs).")

                    if data_split[2] == "1":
                        conn.send(b"* 1 FETCH (BODY[] {1128}\r\n")
                        conn.send(example_mail.encode() + b"\r\n")
                        conn.send(f"{data_split[0]} OK Fetch completed (0.000 + 0.000 + 0.000 secs).".encode())
                    else:
                        conn.send(data_split[0].encode() + b" BAD Error in IMAP command FETCH: Invalid messageset (0.000 + 0.000 secs).")
                elif data_split[1].upper() == "STORE" and authenticated:
                    conn.send(data_split[0] + b" OK Store completed (0.000 + 0.000 secs).")
                elif data_split[1].upper() == "SEARCH" and authenticated:
                    if data_split[2].upper() == "UNSEEN":
                        conn.send(b"* SEARCH 1\r\n")
                        conn.send(data_split[0].encode() + b" OK Search completed (0.002 + 0.000 + 0.001 secs).\r\n")
                    else:
                        conn.send(data_split[0].encode() + b" BAD Error in IMAP command SEARCH: Unknown argument (0.000 + 0.000 secs).\r\n")
                else:
                    conn.send(data_split[0].encode() + b" BAD Error in IMAP command received by server.\r\n")

            conn.close()

if __name__ == '__main__':
    main()
