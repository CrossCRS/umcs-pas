#!/bin/usr/env python
import socket
import ssl

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

    # create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('./GeoTrustGlobalCA.pem')

    # check SNI extension
    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock)

    cert = secure_sock.getpeercert()
    print cert

    if not cert or ('commonName', HOST) not in cert['subject'][4]: raise Exception("Invalid SSL cert for host %s. Check if this is a man-in-themiddle attack!" )

    # write to server using secure socket
    secure_sock.write('GET / HTTP/1.1\r\nHOST: google.com\r\n\r\n')

    # read from secure socket
    print recv_all_until(secure_sock, '\r\n\r\n').split('\r\n')

    secure_sock.close()
    sock.close()
