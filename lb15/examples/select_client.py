#!/usr/bin/env python

import socket
import sys

HOST = '127.0.0.1'
PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)

try:

    while True :

        message = raw_input("> ")
        sock.sendall(message)

        data = sock.recv(4096)
        print "FROM SERVER: %s" % data

finally:
    sock.close()