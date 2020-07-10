import socket
import os
import pickle
import threading


IP = socket.gethostname()
PORT = 5000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(5)


def connection(client):
    try:
        client.send(bytes("Connected successfully. Please enter the name of the desired file","utf-8"))
        k = client.recv(1024).decode("utf-8")
        if k == "DOWNLOAD":
            list_of_files = os.listdir(r"C:\Users\mitth\PycharmProjects\sockets")
            data = pickle.dumps(list_of_files)
            client.send(data)
            file_name = client.recv(1024).decode("utf-8")
            if os.path.exists(file_name):
                client.send(bytes("True", "utf-8"))
                with open(file_name,"rb") as file:
                    file_bytes = file.read()
                    client.send(file_bytes)
            else:
                client.send(bytes("False", "utf-8"))
        elif k == "UPLOAD":
            list_of_files = os.listdir(r"C:\Users\mitth\PycharmProjects\sockets")
            data = pickle.dumps(list_of_files)
            client.send(data)
            file_head = client.recv(2 ** 32).decode("utf-8")
            file_data = client.recv(2 ** 32)
            with open(file_head, "wb") as f:
                f.write(bytes(file_data))
                f.close()
        else:
            pass
    except Exception as e:
        print(e)
        pass


while True:
    connected_socket, addr = s.accept()
    print(addr, "Has joined")
    threading.Thread(target=connection, args=(connected_socket,)).start()


