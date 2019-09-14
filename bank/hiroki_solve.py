#!/usr/bin/env python
from pwn import *
from schnorr import *
import itertools
import string

def encode(data):
    return data.encode('base64').replace('\n', '')

def sha1(teststr):
    ha = hashlib.sha1()
    ha.update(teststr)
    return ha.hexdigest()

def shacheck(teststr):
    digest = sha1(teststr)

    return digest.endswith('0000')

def proofofwork():
    s.recvuntil('with ')
    head = s.recvline(False)
    log.info(head)
    for v in itertools.permutations(string.letters, 5):
        suffix = ''.join(v)

        ans = head + suffix
        if shacheck(ans):
            break
    log.info(sha1(ans))

    s.send(ans)

if len(sys.argv) == 1:
    s = remote('localhost', 20014)
else:
    s = remote('tcp.realworldctf.com', 20014)

proofofwork()

sk, pk = 1, G
s.sendlineafter('Please tell us your public key:', encode('%d,%d' % pk))
s.sendline(encode('1'))
s.sendlineafter('signature', encode(schnorr_sign('DEPOSIT', sk)))
s.sendlineafter('Please tell us your public key:', encode('%d,%d' % pk))
s.sendline(encode('3'))
s.recvuntil('us: (')
pk = (int(s.recvuntil(', ')[:-3]), int(s.recvuntil(')')[:-2]))
pk = (pk[0], -pk[1])
pk = point_add(pk, G)
s.sendlineafter('Please tell us your public key:', encode('%d,%d' % pk))
s.sendline(encode('2'))
s.sendlineafter('signature', encode(schnorr_sign('WITHDRAW', sk)))

s.interactive()
