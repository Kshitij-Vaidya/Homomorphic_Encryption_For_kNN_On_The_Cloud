import socket
import json

PORT = 65433
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'  #utf-8 is an encoding system
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen()

print(f'[SERVER]Listening on {ADDR}')

while True:
    conn,addr = server.accept()
    print(f'[SERVER]{addr} Connected')

    connected = True
    while connected:
        data = json.loads(conn.recv(2048).decode(FORMAT))  #Data receiver from Query User
        print("[SERVER]Received Data")

        print("[SERVER]Running...")
        prime_factorisation = []
        temp_result = list(factor(data["Data"]))
        length = len(temp_result)
        for i,j in temp_result:
            for k in range (0,int(j)):
                prime_factorisation.append(int(i))
        data["Data"] = prime_factorisation
        conn.sendall(json.dumps(data).encode(FORMAT))

        print("[SERVER]Sending Data")
        conn.sendall(json.dumps(data).encode(FORMAT))

        connected = False
    print(f"[SERVER]{addr} disconnected")