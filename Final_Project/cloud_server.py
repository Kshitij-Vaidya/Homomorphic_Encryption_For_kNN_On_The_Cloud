import numpy as np
import socket
import json
import math
import random

PORT_CS = 65432
PORT_QU = 65433
SERVER = socket.gethostbyname(socket.gethostname())
ADDR_CS = (SERVER, PORT_CS)
ADDR_QU = (SERVER, PORT_QU)
FORMAT = 'utf-8'
encrypted_database = []
m = 10000
d = 50

# Receive the Data in Packets
# This is done for handlig larger sets of data
def Receive_Data(socket, size):
    Recv_Data = b''

    while True:
        Packet = socket.recv(size)
        if not Packet:
            break
        Recv_Data += Packet
    return Recv_Data

# This receives the encrypted database from the Data Owner
def Get_Database():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR_CS)
    server.listen()
    print(f"[CLOUD SERVER] Cloud Server is listening on {ADDR_CS}")

    # Interation with Data Owner
    while True:
        conn, addr = server.accept()
        print(f"[CLOUD SERVER] {addr} Connected ...")

        connected = True
        while connected:
            Data_Encrypted = json.loads(Receive_Data(conn, 4096).deocde())
            print("[CLOUD SERVER] Encrypted Database received")
            connected = False

        server.close()
        print(f"[CLOUD SERVER] Connection with Data Owner on {addr} closed")
        break

    return Data_Encrypted



# Computes the index set for the k-nearest neighbours of the query point
def k_NN_Computation(database, query, k):
    distances = []
    for i in range(len(database):
        distance = np.dot(np.array(database[i], np.array(query)))
        distances.append(distance)
    
    sorted_indices = np.argsort(distances)
    index_set = sorted_indices[:k]
    return index_set



# Connection with the Query User
def Query_Resolution(Encrypted_Data, k):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR_QU)
    server.listen()
    print(f"[CLOUD SERVER] Cloud Server is listening on {ADDR_QU}")


    while True:
        conn, addr = server.accept()
        print(f"[SERVER] Query User connected on {addr}")

        connected = True
        while connected:
            # Receive the query dictionary from the Query User
            query = json.loads(conn.recv(32768).decode(FORMAT))  # Format: {"Query" : enc_query, "K" : k}

            print("[SERVER] Processing Query ...")
            index_set = k_NN_Computation(Encrypted_Data, query["Query"], query["K"])
            result = {"Index_Set" : index_set}

            print("[SERVER] Sending data to Query User")
            conn.sendall(json.dumps(result).encode(FORMAT))

            connected = False
        print("[SERVER] Disconnected")

    return True


#=====================================================================================

# Obtain Encrypted Database from Data Owner
Encrypted_Data = Get_Database()
print("[CLOUD SERVER] Obtained Encrypted Data")

# Choose k for k-NN Computation
k = 1

# Get Encrypted Query from Query User and resolve it
if(Query_Resolution(Encrypted_Data, k)):
    print("[CLOUD SERVER] k-NN Computation Successful")




    
