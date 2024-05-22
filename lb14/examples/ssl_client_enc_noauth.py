#!/bin/usr/env python
import socket, ssl

def recv_all_until(secure_sock, crlf):
    data = ""
    while not data.endswith(crlf):
        data = data + secure_sock.read(1)
    return data

if __name__ == '__main__':

    HOST = 'www.google.com'
    PORT = 443

    # create a regular socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # do connect
    sock.connect((HOST, PORT))

    # create ssl context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    # check SNI extension
    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock)

    # write to server using secure socket
    secure_sock.write('GET / HTTP/1.1\r\nHOST: google.com\r\n\r\n')

    # read from secure socket
    print recv_all_until(secure_sock, '\r\n\r\n')

    secure_sock.close()
    sock.close()
