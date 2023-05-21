import socket
import json

PORT = 65433
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'  #utf-8 is an encoding system
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def is_prime(y):
    for i in range(2,y):
        if y%i==0:
            return 1
    return 0

def next_prime(x):
    x +=1
    while is_prime(x):
        x +=1
    return x

def prime_factorisation(x):
    p = 2
    factorisation = []
    while x>1:
        while x%p==0:
            x /= p
            factorisation.append(p)
        p = next_prime(p)
    return factorisation

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
        data["Data"] = prime_factorisation(data["Data"])

        print("[SERVER]Sending Data")
        conn.sendall(json.dumps(data).encode(FORMAT))

        connected = False
    print(f"[SERVER]{addr} disconnected")