#!/usr/bin/env python3
from socket import *

IP = "54.153.22.136"
PORT = 3343

sock = socket(AF_INET, SOCK_STREAM)

sock.connect((IP, PORT))

# READ
s = sock.recv(1024)
print(s)

# WRITE
s = "foo\n"
sock.send(s.encode())
s = sock.recv(1024)
print(s)
