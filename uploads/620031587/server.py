'''
620031587
Simple Python HTTP Server
'''
import socket 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9000
#Prepare a server socket
server_socket.bind(('', port))
server_socket.listen(1)

while True:
    #Establish the connection
    print 'Ready to serve...'
    conn_socket, addr = server_socket.accept()
    message = conn_socket.recv(1024)
    #Prevent server from crashing when no requests are sent
    if message is None:
        continue
    filename = message.split()[1][1:]
    #Serve page
    try:
        f = open(filename)
        status_code = '200 OK'
    except IOError:
        f = open('404.html')
        status_code = '404'
    finally:
        with f:
            content = f.read()
            headers = 'HTTP/1.1 %s\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %d\r\n\r\n' % (status_code, len(content))
            #Send headers and page content
            conn_socket.send(headers)
            conn_socket.send(content)
        conn_socket.close()
