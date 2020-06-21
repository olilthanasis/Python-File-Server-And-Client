import socket
import os
import time


IP = socket.gethostname() #Test IP
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(5)
while True:
    connected_socket, addr = s.accept()
    connected_socket.send(bytes("Connected successfully; please enter the name of the desired file","utf-8"))

    file_name = connected_socket.recv(1024).decode("utf-8")
    if os.path.exists(file_name):
        connected_socket.send(bytes("True", "utf-8"))
        with open(file_name,"rb") as file:
            file_bytes = file.read()
            connected_socket.send(file_bytes)

