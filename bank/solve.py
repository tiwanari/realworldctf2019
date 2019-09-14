#!/usr/bin/env python

from socket import *
import string
import hashlib
import logging
import itertools
import random
import os
import base64 as b64
import calendar
import datetime

from schnorr import generate_keys, schnorr_verify, point_add

MSGLENGTH = 40000
HASHLENGTH = 16

letters = string.ascii_letters + string.digits

logging.basicConfig(level=logging.DEBUG)

def shacheck(teststr):
    ha = hashlib.sha1()
    ha.update(teststr.encode())

    return ha.digest()[-1] == 0 and ha.digest()[-2] == 0 and ha.digest()[-3] == 0 and ha.digest()[-4] == 0

def first_stage(proof, test):
    ha = hashlib.sha1()
    ha.update(test)

    logging.info(len(proof), len(test))

    if test[0:16] != proof:
        logging.info("not proof")
        return False

    elif ha.digest()[-1] != 0:
        logging.info("1 Check failed")
        return False

    elif ha.digest()[-2] != 0:  # or ord(ha.digest()[-3]) != 0 or ord(ha.digest()[-4]) != 0):
        logging.info("2 Check failed")
        return False

    return True


def second_stage():
    logging.info("Generating keys...\n")

    sk, pk = generate_keys()
    balance = 0

    while True:
        logging.info("Please tell us your public key:")
        message = "MTExMTExMSwyMjIyMjI="
        logging.info("got " + message)
        msg = message.strip().decode('base64')
        logging.info(msg)
        if len(msg) < 6 or len(msg) > MSGLENGTH:
            logging.info("what are you doing?")
            return
        userPk = (int(msg.split(',')[0]), int(msg.split(',')[1]))
        logging.info('''User logged in.

                [Beep]

    Please select your options:

    1. Deposit a coin into your account, you can sign a message 'DEPOSIT' and send us the signature.
    2. Withdraw a coin from your account, you need to provide us a message 'WITHDRAW' signed by both of you and our RESPECTED BANK MANAGER.
    3. Find one of our customer support representative to assist you.


    Our working hour is 9:00 am to 5:00 pm every %s!
    Thank you for being our loyal customer and your satisfaction is our first priority!
    ''' % calendar.day_name[(datetime.datetime.today() + datetime.timedelta(days=1)).weekday()])

        message = input("menu: ")
        base64 = {1:"MQ==", 2:"Mg==", 3:"Mw=="}
        msg = base64[message].decode('base64')
        if msg[0] == '1':
            logging.info("Please send us your signature")

            message = input("signature: ")
            msg = message.strip().decode('base64')
            if schnorr_verify('DEPOSIT', userPk, msg):
                balance += 1
            logging.info("Coin deposited.\n")

        elif msg[0] == '2':
            logging.info("Please send us your signature")

            message = input("signature: ")
            msg = message.strip().decode('base64')
            if schnorr_verify('WITHDRAW', point_add(userPk, pk), msg) and balance > 0:
                logging.info("Here is your coin: %s\n" % "yay!")

        elif msg[0] == '3':
            logging.info("The custom service is offline now.\n\nBut here is our public key just in case a random guy claims himself as one of us: %s\n" % repr(pk))


def solve___():
    IP = "tcp.realworldctf.com"
    PORT = 20014

    sock = socket(AF_INET, SOCK_STREAM)

    sock.connect((IP, PORT))

    # first step
    s = sock.recv(1024)

    sock.send(solve_fisrt(s))

    s = sock.recv(1024)
    logging.info(s)

    # second_stage()


def solve_fisrt(s):
    logging.info(str(s))
    recv = s[120:-1]  # 最初の16文字の部分

    head = recv.decode()
    logging.info(head)
    logging.info(len(head))

    # head + 5 characters
    ans = head + 'xxxxx'
    l = list(letters)
    for v in itertools.permutations(l, 5):
        suffix = ''.join(v)
        logging.debug(suffix)

        ans = head + suffix
        if shacheck(ans):
            break

    logging.debug('found !' + ans)
    logging.info(len(ans))

    return ans.encode()


def solve():
    second_stage()


if __name__ == "__main__":
    solve()
