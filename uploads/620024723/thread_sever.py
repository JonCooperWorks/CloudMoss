#620024723

from socket import *
from threading import *


serverSocket = socket(AF_INET, SOCK_STREAM) 

#Prepare a sever socket 
TCP_BUFFER = 1024
TCP_PORT = input("What port shall i serve you from? ")

serverSocket.bind(('', TCP_PORT))
serverSocket.listen(1)

# Displays pages
def getPage (conSocket, page):
    
    try:
        f = open(page)
    
    except IOError:
        f = open('404.html')
            
    finally:
        with f:
            content = f.read()
            headers = 'HTTP/1.1 \r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %d\r\n\r\n' % (len(content))
             
            conSocket.send(headers)
            for i in content:
                conSocket.send(i)
        conSocket.close()

# Info about current connection

def getConnection(serSocket):
    
    conSocket, addr = serSocket.accept()
    
    message = conSocket.recv(TCP_BUFFER)
    
    if message is None:
        return None
    return conSocket, message.split()[1][1:]



while True:
    
    print 'Ready to serve...'
    
    # Gets arguments for python threading module
    args = getConnection(serverSocket)

    # Stops the server from crashing when 'args' has no value
    if args is None:
        continue

    # Threading here
    Thread(target=getPage, args=args).start()
