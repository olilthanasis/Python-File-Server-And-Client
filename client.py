import socket
import tkinter as tk
from tkinter import filedialog
import pickle

IP = socket.gethostname()
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
print(s.recv(1024).decode("utf-8"))
getorpush = input("Do you wish to upload or download a file? ")

if getorpush.lower() == "download":
    s.send(bytes('DOWNLOAD', "utf-8"))
    list_of_files = pickle.loads(s.recv(2**32))
    print("Here is a list of all available files: ")
    for i in list_of_files:
        print(i)
    file_name = input(">>>")
    s.send(bytes(file_name,"utf-8"))
    file_exists =s.recv(1024).decode("utf-8")
    if file_exists == "True":
        print(f"{file_name} found. We are sending it over")
        print("save file as(do not use spaces): ")
        root = tk.Tk()
        root.lift()
        file_path = filedialog.asksaveasfile()
        file_path = str(file_path).split()[1][6:-1]
        file_data = s.recv(2**32)
        with open(file_path,"wb") as file:
            file.write(file_data)
        print(f"file saved at {file_path}")
        s.close()
    else:
        print("file was not found")
        s.close()
elif getorpush.lower() == "upload":
    s.send(bytes('UPLOAD',"utf-8"))
    list_of_files = pickle.loads(s.recv(2**32))
    print(list_of_files)
    root = tk.Tk()
    root.lift()
    file_path = filedialog.askopenfilename()
    name = input("File Name: ")
    if name in list_of_files:
        print(f"{name} already exists. Try another name.")
        s.close()
        quit()
    with open(file_path,"rb") as file:
        file_data = file.read()
    s.send(bytes(name,'utf-8'))
    s.send(file_data)
    s.close()
else:
    s.close()
    print(f"ERROR :{getorpush}<---- illegal command \nTry using either 'upload' or 'download'")
