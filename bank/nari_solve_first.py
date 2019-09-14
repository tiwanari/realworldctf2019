#!/usr/bin/env python

import hashlib
import logging
import string
from socket import *
import numpy
from sklearn.utils.extmath import cartesian
import multiprocessing

MSGLENGTH = 40000
HASHLENGTH = 16

letters = string.ascii_letters + string.digits

logging.basicConfig(level=logging.DEBUG)


def shacheck(teststr):
    ha = hashlib.sha1()
    ha.update(teststr.encode())

    return ha.digest()[-1] == 0 and ha.digest()[-2] == 0  # and ha.digest()[-3] == 0 and ha.digest()[-4] == 0


def solve():
    IP = "tcp.realworldctf.com"
    PORT = 20014

    sock = socket(AF_INET, SOCK_STREAM)

    sock.connect((IP, PORT))

    # first step
    s = sock.recv(1024)

    sock.send(solve_first(s))

    s = sock.recv(1024)
    logging.info(s)

    # second_stage()


def solve_first(s):
    logging.info(str(s))
    recv = s[120:-1]  # first 16 characters

    head = recv.decode()
    logging.info(head)
    logging.info(len(head))

    # head + 5 characters
    ans = head + 'xxxxx'
    l = list(letters)
    # for v in itertools.product(l, repeat=5):
    #     suffix = ''.join(v)
    #     logging.debug(suffix)
    #
    #     ans = head + suffix
    #     if shacheck(ans):
    #         break

    # for v in cartesian((l, l, l, l)):
    #     suffix = ''.join(v)
    #     logging.debug(suffix)

    #     ans = head + suffix
    #     if shacheck(ans):
    #         break

    four_chars = cartesian((l, l, l, l))
    for v in four_chars:
        for x in list(l):
            suffix = ''.join(v) + x
            logging.debug(suffix)

            ans = head + suffix
            if shacheck(ans):
                break

    logging.debug('found !' + ans)
    logging.info(len(ans))

    return ans.encode()


if __name__ == "__main__":
    solve()
