#!/usr/bin/env python3

"""
Client for assignment 1
"""

import socket
import sys
import Payload as pl


def getSocket(address, port):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address, port))
    except socket.error as message:
        if s:
            s.close()
        print("Error opening client socket: " + str(message))
        sys.exit(1)
    return s


def getAnswer(question, address, port):
    soc = getSocket(address, port)
    soc.send(pl.getPayload(question))
    answers = []
    answerPayload = soc.recv(1024)
    answertext = pl.getText(answerPayload)
    answers.append(answertext)
    try:
        while 1:
            answerPayload = soc.recv(1024)
            answertext = pl.getText(answerPayload)
            answers.append(answertext)
    except:
        soc.close()
    if answers:
        return answers
    else:
        print("Error receiving answer")
        return None

print('Received:', getAnswer("Here's the first question", 'localhost', 50000))
print('Received:', getAnswer("Here's the second question", 'localhost', 50000))
