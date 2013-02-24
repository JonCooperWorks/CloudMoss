#ID: 620045541
#import socket module

from socket import *
from threading import *


def serverfunc(connectionSocket, output, headers):
    connectionSocket.send(headers)
    connectionSocket.send(output)
connectionSocket.close()


serverSocket = socket(AF_INET, SOCK_STREAM)

PORT = 8080
serverSocket.bind(('', PORT))

serverSocket.listen(1)
while True:
    #Establish the connection
    print 'Ready to serve...'
   
    connectionSocket, addr = serverSocket.accept()
    try:
       
        message = connectionSocket.recv(1024)
        
        if message == None:
            continue

        filename = message.split()[1]
        f = open(filename[1:])
      
        output = f.read()
        f.close()
        #Send one HTTP header line into socket
       
        header1 = Thread(target= serverfunc, args=(connectionSocket, output, 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %d\r\n\r\n' % len(output)))
        header1.start()
    except IOError:
        #Send response message for file not found
               
        errormessage = "File Not Found"

        header = Thread(target= serverfunc, args=(connectionSocket, output, 'HTTP/1.1 404\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %d\r\n\r\n' % len(output)))
        header.start()
serverSocket.close()
