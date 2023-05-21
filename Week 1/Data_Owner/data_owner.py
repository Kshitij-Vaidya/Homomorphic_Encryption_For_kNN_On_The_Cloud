import socket
import random
import json

PORT = 65432
#Use the below line of code to get the host IP address
#Makes is easier to use the code on multiple devices
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!!Disconnect"

#SOCK_STREAM is used to indicate TCP
data_owner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_owner.bind(ADDR)

print("[DATA OWNER] Data Owner is starting...")
data_owner.listen()

print(f"[DATA OWNER]Listening on {ADDR}")

#Sequential handling of multiple queries
while True:
    conn,addr = data_owner.accept()
    print(f"[DATA OWNER]Connected {addr}")

    connected  = True
    while connected:
        query = json.loads(conn.recv(2048).decode(FORMAT))

        rand_num = random.randint(1,10000)

        query["Data"] *= rand_num

        conn.sendall(json.dumps(query).encode(FORMAT))
        connected = False

    print(f'{addr} Disconnected')




