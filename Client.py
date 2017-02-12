#!/usr/bin/env python3

"""
Client for assignment 1
"""
import pickle
import hashlib
import socket
import sys

def getPayload(text):
    tup = (text, hashlib.md5(text.encode('utf-8')).hexdigest())
    payload = pickle.dumps(tup)
    return payload


def getText(payload):
    tup = pickle.loads(payload)
    text = tup[0]
    transmittedCheck = tup[1]
    calculatedCheck = hashlib.md5(text.encode('utf-8')).hexdigest()
    if transmittedCheck != calculatedCheck:
        print("Error unpacking payload: calculated checksum did not match received checksum")
        return None
    return text


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
    print("Client socket opened")
    return s


def getAnswer(question, address, port):
    soc = getSocket(address, port)
    print("Client sending question: " + question)
    soc.send(getPayload(question))
    answers = []
    answerPayload = soc.recv(1024)
    answertext = getText(answerPayload)
    answers.append(answertext)
    print("Client recieved answer: " + answertext)
    try:
        while 1:
            answerPayload = soc.recv(1024)
            answertext = getText(answerPayload)
            answers.append(answertext)
            print("Client recieved answer: " + answertext)
    except:
        soc.close()
        print("Client socket closed")
    if answers:
        return answers
    else:
        print("Error receiving answer")
        return None

print('Received:', getAnswer("Here's the first question", 'localhost', 50000))
print('Received:', getAnswer("Here's the second question", 'localhost', 50000))
