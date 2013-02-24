'''
620031587
Simple Python HTTP Server
'''
import socket
import threading

#Factor out common page serving logic to function
def serve(conn_socket, page):
    try:
        f = open(page)
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


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9000
#Prepare a server socket
server_socket.bind(('', port))
server_socket.listen(1)

while True:
    #Get the connection socket and filename
    conn_socket, addr = server_socket.accept()
    msg = conn_socket.recv(1024)
    print msg
    #No request sent. Stop server from crashing upon recv() timeout
    if msg is None:
        continue
    filename = msg.split()[1][1:]
    args = (conn_socket, filename)
    #Spawn a new thread to handle request. New connection object will be created at next iteration.
    threading.Thread(target=serve, args=args).start()
