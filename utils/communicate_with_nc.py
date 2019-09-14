#!/usr/bin/env python3

# CTF では nc コマンドで対話的なやり取りすることがある
# そのときに向こうからのデータを受け取ったり
# 受け取ったデータを処理して返したり
# というのをスクリプトでやれると楽なのでこれを使ってくださいな
from socket import *

IP = "vermatrix.pwn.democrat"
PORT = 4201

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
