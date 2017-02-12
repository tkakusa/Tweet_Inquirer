#!/usr/bin/env python3

"""
Server for assignment 1
"""
import pickle
import hashlib
import wolframalpha
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

def wolframQuery(query):
    try:
        # create wolfram alpha client service
        wolframService = wolframalpha.Client("9KL76E-2P62RRAAJ2")
        print("[DBG] Asking Wolfram the question.")

        # send the question through the wolfram alpha api
        answerPackage = wolframService.query(query)
    except Exception:
        return ["[ERR] There was a problem connecting to Wolfram Alpha."]
    else:
        print("[DBG] Got answer back.")

        # get answer from wolfram alpha
        try:
            results, = answerPackage.results
        except AttributeError:
            return ["[ERR] Wolfram Alpha did not understand your query."]
        else:
            print("[DBG] Extracting results.")
            # Extract the actual text of the answer
            answer = results.text

            # Split multiple answers
            answerList = re.split("\n[0-9] \| ", answer)

            # Put the numbers back on the front of the multiple answers that split() removed
            i = 1
            for multAnswer in answerList:
                if(i > 1):
                    answerList[i - 1] = (str(i) + " | " + multAnswer)
                i = i + 1;

            # Return the complete list of answers
            return answerList


host = ''
port = 50000
backlog = 5
size = 1024
s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(backlog)
except socket.error as message:
    if s:
        s.close()
    print("Could not open socket: " + str(message))
    sys.exit(1)
print("Server socket opened on port 50000")
while 1:
    client, address = s.accept()
    print("Server accepted client connection")
    data = client.recv(size)
    if data:
        question = getText(data)
        if question:
            print("Server received question: " + question)
            answerList = {"Here's the first answer", "Here's a second answer"} #replace with wolfram call
            for answer in answerList:
                print("Server sending answer:" + answer)
                answerPld = getPayload(answer)
                client.send(answerPld)
        else:
            print("Error receiving question")
    client.close()
