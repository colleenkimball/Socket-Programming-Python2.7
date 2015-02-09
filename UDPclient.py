'''
UDPclient.py
Author: Colleen Kimball
Date: November 2, 2014
Description: This program connects to a server using UDP and pings the server 10 times, collecting RTT information and recording it. 
'''

from socket import*
import time
import threading

#this function sends a ping message to the server and records the RTT
def ping(num, rtt):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    #set timeout to 1 second
    clientSocket.settimeout(1)
    #message must be in byte form
    message=b'Ping';
    start=time.time()
    clientSocket.sendto(message, ('localhost',12000))
    try:
        message,address = clientSocket.recvfrom(2048)
        #elapsed is RTT
        elapsed=(time.time()-start)
        print (str(num)+' Message: '+message+'  RTT: '+str(elapsed)+'\n')
    except timeout:
        #set elapsed to -1 and check for it later so it doesn't skew data
        elapsed=-1
        print (str(num)+ ' Request Timed Out'+'\n')
    clientSocket.close()
    rtt.append(elapsed)
    
def main():
    threads=[]
    rtt=[]
    for i in range(10):
        
        #each thread pings the server
        t=threading.Thread(target=ping, args=(i,rtt,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    avg=0
    lost=0
    minimum=rtt[0]
    for time in rtt:
        if time!=-1:
            avg+=time
            if minimum>time:
                minimum=time
        else:
            lost+=1
    avg/=len(rtt)
    print ('RTT: Minimum: '+str(minimum)+' Maximum: '+str(max(rtt))+' Average: '+str(avg) + ' Lost: '+str(lost)+'\n')
    print("main  finished")

        
main()
