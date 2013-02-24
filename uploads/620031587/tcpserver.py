import socket
import sys

server_socket = socket.socket((socket.AF_INET, socket.SOCK_STREAM))
server_socket.bind(('', 8080))
server_socket.listen(1)

while True:
    conn_socket, addr = server_socket.accept()
    msg = conn_socket.recv(1024)
    print msg
    conn_socket.send(msg)
    