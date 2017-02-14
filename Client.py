from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
import pickle
import socket
import json
import re
import sys
import unicodedata
import hashlib

ckey =	'DhZMPy4JdoHXE0fjoaZq8UESZ'
csecret = 'xd5XanwZ1dn2OMpO9aBrEI7XKiw2XaZyhYpnsUly5Db5ol797t'
atoken = '4856679433-ZvQquWCdv4TftB13vCmcrn88gWSWe2iBscbf00o'
asecret = '3QT3g5tV4XjbgxxCDsd7YobwfhGDTxenYvmGtCYSvst0v'
question = ''

#sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sender.connect(('172.25.19.231', 2000))

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

def messageParser(line):
    tweeter = re.search('(?<=@)\w+', line)
    ipaddr = re.search('(?<=#)[0-9.]*', line)
    portaddr = re.search('(?<=:)[0-9]*', line)
    message = re.search('(?<=\_).*', line)
    message2 = re.sub('\”','',message.group(0))
    message3 = re.sub('\"','',message2)
    return (tweeter, ipaddr.group(0), portaddr.group(0), message3)
    

class listener(StreamListener):

    def on_data(self, data):
        line = json.loads(data)
        (tweeter, ipaddr, portaddr, message) = messageParser(line['text'])
        question = message
        print ('got the message ', question)
        print ('Got IP Address  ', ipaddr)
        answer = getAnswer(str(question), str(ipaddr), int(portaddr))
        print ('Got the Answer')
        for tweet in answer:
            response = '@VTNetApps Team_03 "' + tweet +'"'
            shortened = response[:130] + (response[130:] and '..')
            api.update_status(shortened)
        return True

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth)
twitterStream = Stream(auth, listener())
question = twitterStream.filter(track=["tomjones356"])
while (1):
    if (question != ''):
        print (question)
        question = ''
