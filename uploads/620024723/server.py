#620024723

from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM) 

#Prepare a sever socket 
TCP_BUFFER = 1024
TCP_PORT = input("What port shall i serve you from? ")

serverSocket.bind(('', TCP_PORT))
serverSocket.listen(1)

while True:
    
    #Establish the connection
    print 'Ready to serve...'
    connectionSocket, addr = serverSocket.accept()
    
    try:
        message = connectionSocket.recv(TCP_BUFFER)

        #Prevent server from crashing when no requests are sent
        if message is None:
            continue

        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        
        #Send one HTTP header line into socket
        headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %d\r\n\r\n' % len(outputdata)
        connectionSocket.send(headers)
        
        #Send the content of the requested file to the client
        for char in outputdata:
            connectionSocket.send(char)
    
    except IOError:
        
        #Send response message for file not found
        f=  open('404.html')
        content = f.read()
        headers = 'HTTP/1.1 404\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %d\r\n\r\n' % len(content)
        connectionSocket.send(headers)
        
        for char in content:
            connectionSocket.send(char)
    
    finally:
        #Close client socket
        connectionSocket.close()
