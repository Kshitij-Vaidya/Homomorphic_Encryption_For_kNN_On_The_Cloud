import socket
import json

PORT1 = 65432
PORT2 = 65433
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!!DISCONNECT"
SERVER = socket.gethostname()
ADDR_DATA_OWNER = (SERVER, PORT1)
ADDR_SERVER = (SERVER, PORT2)
data = []
query_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


x = int(input("Enter a positive integer: "))
query = {"Data": x}

# Interaction of QUERY USER and DATA OWNER

query_user.connect(ADDR_DATA_OWNER)
query_user.sendall(json.dumps(query).encode(FORMAT))  #Sending query to the data owner

data = json.loads(query_user.recv(2048).decode(FORMAT))

print(f'[QUERY USER]Modified Integer: {data["Data"]}')

query_user.close()  #Closes the connection with the data owner

#Interaction of QUERY USER and SERVER

query_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Initializes the socket object agaion for the server

query_user.connect(ADDR_SERVER)
query_user.sendall(json.dumps(data).encode(FORMAT))

print("Data sent for factorisation")