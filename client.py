import socket


IP = socket.gethostname() #Test IP
PORT = 5000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
print(s.recv(1024).decode("utf-8"))
file_name = input(">>>")
s.send(bytes(file_name,"utf-8"))
file_exists =s.recv(1024).decode("utf-8")
if file_exists == "True":
    print(f"{file_name} found. We are sending it over")
file_data = s.recv(2**32)
with open(file_name,"wb") as file:
    file.write(file_data)
s.close()



