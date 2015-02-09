"""
Created by Colleen Kimball
September, 2014
Ithaca, NY

This program is a simple example of creating a server socket and client socket and 
outputting a website to the client. 

"""
import socket
import sys
 
HOST = 'localhost'   
PORT = 8889 # Arbitrary non-privileged port
 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
 
try:
    serverSocket.bind((HOST, PORT))
except socket.error :
    print ('Bind failed. ' )
    sys.exit()
     
print ('Socket bind complete')
 
serverSocket.listen(10)
print ('Socket now listening')

while True:
    #Establish the connection
    print 'Ready to serve...'
    connectionSocket, addr = serverSocket.accept()

    try:
        message =connectionSocket.recv(2048)
        if(message!=''):
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.readlines()
            #Send one HTTP header line into socket
            out = 'HTTP/1.1 200 OK \r\n'
            connectionSocket.send(out)
            connectionSocket.send('\r\n')
       
            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i])
            connectionSocket.close()
    except IOError:
        #Send response message for file not found
        filename="404.html"
        f = open(filename)
        out = 'HTTP/1.1 404 Not Found \r\n'
        outputdata = f.readlines()
        connectionSocket.send(out)
        connectionSocket.send('\r\n')
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
        connectionSocket.close()

serverSocket.close()
connectionSocket.close()
