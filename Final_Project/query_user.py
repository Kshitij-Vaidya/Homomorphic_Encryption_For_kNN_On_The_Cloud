import json
import socket 
import numpy as np
from sympy import randprime
import random
import sage
import math

PORT_CS = 65432
PORT_DO = 65433
SERVER = socket.gethostbyname(socket.gethostname())
ADDR_CS = (SERVER, PORT_CS)
ADDR_DO = (SERVER, PORT_DO)
FORMAT = 'utf-8'
d = 50
m = 10000


class Paillier:
    def __init__(self, k = 1024):
        self.k = K

        # L(x) function 
        def L_x(x, n):
            return (x - 1) //  n

        while(True):
        # Generation of 2 distinct primes such that GCD(pq, (p-1)(q-1)) = 1
            self.p = int(random_prime(2 ** self.k))
            while(True):
                self.q = int(random_prime(2 ** self.k))

                if(self.p == self.q or gcd(self.p*self.q , (self.p - 1)*(self.q - 1)) != 1) : continue
                else : break

            self.N = self.p * self.q

            self.L = lcm(self.p - 1, self.q - 1)

            # Compute the generator number
            self.G = randint(1, self.N**2 - 1)

            while(gcd(self.g, self.n) != 1):
                self.g = randint(1, self.N**2)


            # Computation of Modular Multiplicative Inverse 
            if (gcd(L_x(int(pow(self.G, self.L, self.N**2)), self.N), self.N)) == 1:
                self.Mu = inverse_mod(int(L_x(pow(self.G, self.L, self.N**2)), self.N), self.N)
                break
            else:
                continue

    
    def get_public_key(self):
        return self.N, self.G
    
    
    # Perform Paillier Encryption on the entire query tuple, encrypting each point if the tuple separately
    def Encrypt(self, plaintext):
        self.R = randint(1, self.N - 1)

        if (plaintext >= int(self.N)):
            raise ValueError("Invalid Plaintext")
        else:
            ciphertext = int(mod(power_mod(self.G, plaintext, self.N**2) * power_mod(self.R, self.N, self.N**2), self.N ** 2))

        return ciphertext


    def Decrypt(self, ciphertext):
        if ciphertext >= self.N**2 : 
            raise ValueError("Invalid Ciphertext")
        
        P = power_mod(int(ciphertext), self.L, self.N**2)
        L = self.L_x(P, self.N)

        plaintext = int(mod(int(L) * self.Mu, self.N))

        return plaintext
    

# Define Function to send Encrypted Query to Query User and obtain A_q
def Query_DataOwner(message):
    query_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    query_user.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    query_user.connect(ADDR_DO)

    query_user.sendall(json.dumps(message).encode())
    print("[QUERY USER] Sent the Encrypted Query")

    A_q = json.loads(query_user.recv(32768).decode())

    print("[QUERY USER] Received A_q")

    query_user.close()
    return A_q


# Receive Index Set
def Recv_IndexSet(Q_Dash):
    query_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    query_user.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Establish the connection with the Query User
    query_user.connect(ADDR_CS)

    query_user.sendall(json.dumps(Q_Dash).encode())
    print("[QUERY USER] Sending the Encrypted Query ...")

    Index_Set = json.loads(query_user.recv(32768).decode())
    query_user.close()

    return Index_Set
    

# Define function to manage large streams of data
def Send_Packet(socket, data, size):
    Sent = 0
    while Sent < len(data):
        packet = data[Sent:Sent + size]
        Sent += socket.send(packet)




# Query Input From User
# This is a sample query(Actually the First Datapoint in the Database)
# The query can be modified by the User
Q = [-2952, 9264, -1999, 8672, 6278, 6246, 6699, -2329, -8865, 9105, 9615, 6881, 5655, 167, 7885, -9346, 232, 1222, 7126, -1446, -6620, -3040, -5770, -7051, -1799, -4113, 5703, -7962, 6229, 1457, -1067, -5885, -9128, -8916, -9302, 1249, 2717, 9583, 9623, 4460, -2822, 1455, -7226, -7845, -8713, -7573, 1634, 1285, 185, 376]

print("[QUERY USER] Generated Random Query")

# Eliminating negative values for Paillier Encryption
for i in range(d):
    if Q[i] < 0:
        Q[i] = abs(Q[i]) + 10000

# Generate Public Key for Paillier Encryption
paillier = Paillier(k = 32)

N, G = paillier.get_public_key()

# Get Paillier encrypted query
Pai_Q = [paillier.Encrypt(x) for x in Q]

print("[QUERY USER] Encrypted the Query")

# Sending the Dictionary to the Data Owner containing the query and the public key
Message = {"Query" : Q, "PaillierN" : N, "PaillierG" : G}

A_q = Query_DataOwner(Message)

# Decrypt Received Query using secret Paillier Key
Q_Dec = [paillier.Decrypt(x) for x in A_q]

# Sending the query to the cloud server for k-NN Computation
Index_Set = Recv_IndexSet(Q_Dec)

print(f"Index Set : {Index_Set}")
    






