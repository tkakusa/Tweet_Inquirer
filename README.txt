# Tweet_Inquirer

This program allows the user to send a question via Twitter and receive the answer via Twitter.

To run the program, the Server.py script must be run first on the server machine (raspberry pi), 
then the Client.py script must be run on the client machine. 
Both machines must be connected to the internet, and the scripts must be run with python 3. 

The necessary external python libraries for the client machine are:
  tweepy
  pickle
  socket
  json
  re
  sys
  unicodedata
  hashlib
  
The necessary external python libraries for the server machine are:
  pickle
  hashlib
  wolframalpha
  re
  socket
  sys
  
  The question tweet must be in the following format: @tomjones356 #[server ip address]:50000_"Question text"
    e.g. @tomjones356 #192.168.1.1:50000_"What is a hokie?"
  The answer will be tweeted at the VTNetApps account in the following format: @VTNetApps Team_03 "Answer text"
