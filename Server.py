import socket
import os
import pickle


IP = socket.gethostname()
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(5)

while True:
    connected_socket, addr = s.accept()
    connected_socket.send(bytes("Connected successfully; please enter the name of the desired file","utf-8"))
    if connected_socket.recv(1024).decode("utf-8") == "DOWNLOAD":
        list_of_files = os.listdir(r"C:\Users\mitth\PycharmProjects\sockets")
        data = pickle.dumps(list_of_files)
        connected_socket.send(data)
        file_name = connected_socket.recv(1024).decode("utf-8")
        if os.path.exists(file_name):
            connected_socket.send(bytes("True", "utf-8"))
            with open(file_name,"rb") as file:
                file_bytes = file.read()
                connected_socket.send(file_bytes)
        else:
            connected_socket.send(bytes("False", "utf-8"))
    else:
        list_of_files = os.listdir(r"C:\Users\mitth\PycharmProjects\sockets")
        data = pickle.dumps(list_of_files)
        connected_socket.send(data)
        file_head = connected_socket.recv(2**32).decode("utf-8")
        file_data = connected_socket.recv(2**32)
        with open(file_head, "wb") as f:
            f.write(bytes(file_data))
            f.close()

