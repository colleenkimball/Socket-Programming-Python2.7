"""
Created by Colleen Kimball
October, 2014
This program creates a socket connection and uses threading to receive all of the 
documents included in the HTML page. 

"""
import socket
import sys
import threading

def multiThread(serverSocket, connectionSocket, Host, Port):
    try:
        message =connectionSocket.recv(2048)
        if(message!=''):
            filename = message.split()[1]
			# if the filename is looking in the previous location, send a request for the correct file location
            if filename[1:]=="hello_world.html":
                out = 'HTTP/1.1 301 Moved Permanently \r\n'
                out+='Location: '+str(Host)+':'+str(Port)+'/home/hello_world.html \r\n'
                connectionSocket.send(out)
                connectionSocket.close()
            else:
                f = open(filename[1:])
                print 'opening file: '+filename
                outputdata = f.read()
                #Send one HTTP header line into socket
                out = 'HTTP/1.1 200 OK \r\n'
                
                if filename.split('.')[1]=="jpeg":
                    out +='Content-Type: image/jpeg \r\n'
                elif filename.split('.')[1]=="png":
                    out +='Content-Type: image/png \r\n'
                elif filename.split('.')[1]=="gif":
                    out +='Content-Type: image/gif \r\n'
                out += '\r\n'
                print out
                connectionSocket.send(out)
       
                #Send the content of the requested file to the client
                for i in range(0, len(outputdata)):
                    connectionSocket.send(outputdata[i])
                connectionSocket.close()
            return
    except IOError:
        #Send response message for file not found
        filename="home/404.html"
        f = open(filename)
        out = 'HTTP/1.1 404 Not Found \r\n'
        outputdata = f.readlines()
        connectionSocket.send(out)
        connectionSocket.send('\r\n')
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
        connectionSocket.close()
        return

def main():
 
    HOST = 'localhost'   
    PORT = 8885 # Arbitrary non-privileged port
    
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
    threads=[]
    while True:
        #Establish the connection
        print 'Starting a new thread...'
        connectionSocket, addr = serverSocket.accept()
        t=threading.Thread(target=multiThread, args=(serverSocket, connectionSocket, HOST, PORT, ))
        threads.append(t)
        t.start()
    serverSocket.close()
    connectionSocket.close()

main()
