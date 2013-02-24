#ID: 620045541
#import socket module

from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a socket server
PORT = 8081
serverSocket.bind(('', PORT))
serverSocket.listen(1)
print 'The server is ready to receive'

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
       
        connectionSocket.send( 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %d\r\n\r\n' % len(output))
        
        connectionSocket.send(output)
        
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
             
        errormessage = "File not found"
       
        connectionSocket.send('HTTP/1.1 404\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %d\r\n\r\n' % len(errormessage))
        connectionSocket.send(errormessage)

        #Close client socket
        connectionSocket.close()
serverSocket.close()
