import socket
import json
import random
import numpy as np
import math
import sage

PORT_CS = 65432
PORT_DO = 65433
SERVER = socket.gethostbyname(socket.gethostname())
ADDR_CS = (SERVER, PORT_CS)
ADDR_DO = (SERVER, PORT_DO)
FORMAT = 'utf-8'
PATH = "/Users/kshitijvaidya/Desktop/VirtualEnvironment/SoC_Project/Final_Project/database.txt"

# Generating random parameters
c = random.randint(1, 10)
epsilon = random.randint(1, 10)
d = 50 # No of dimensions in each data point
m = 10000 # No of data points
n = c + epsilon + d + 1
R_q = np.random.randint(-10, 10, c)



# Finds the GCD of two numbers a and b
def GCD(a,b):
    while b != 0:
        a, b = b, a % b
    return a



# Function generates the secret key of the scheme
def PrivateKeyGen():
    M = 1 + np.random.randint(10, size = (n, n)) # Random invertible matrix

    while np.linalg.matrix_rank(M) < n:
       M = 1 + np.random.randint(10, size = (n, n))
    S = np.random.uniform(0, 10, size = d + 1) # Random (d + 1)-dimensional vector
    Tau = np.random.uniform(0, 10, size = c) # Random c-dimensional vector
    Pi = [i for i in range(n)]

    # Convert matrix into a list
    M_List = []
    for row in M:
        L = list(row)
        M_List.append(L)

    # Permutation of numbers in range (0, n)
    for i in range(n):
        j = random.randint(0, n - 1)
        while j == i:
            j = random.randint(0, n - 1)

        temp = Pi[i]
        Pi[i] = Pi[j]
        Pi[j] = temp

    return [M_List, S, Tau, Pi] # Return the secret key


# Inverse Permutation List
def Inverse_Perm(Perm):
    n = len(Perm)
    Inverse = [0] * n

    for i in range(n):
        Inverse[Perm[i]] = i
    
    return Inverse



# Obtains the database from Database.txt
def GetDatabase():
    Database = []
    F = open("Database.txt", "r")
    for line in F:
        row = [int(n) for n in line.strip().split(',')]
        Database.append(row)

    # We need to ensure that our database has no negative values for encryption purposes
    # This is achieved by a cyclic shift of the negative values
    for i in range(m):
        for j in range(d):
            if Database[i][j] < 0:
                Database[i][j] = abs(Database[i][j]) + 10000

    return Database


# Encryption of a Single Datapoint in the Database
def DatapointEnc(Database, i, Key, v):
    Point = Database[i]
    MP2 = 0

    for i in Point:
        MP2 += (i ** 2)

    M = Key[0]
    S = Key[1]
    T = Key[2]
    Perm = Key[3]

    P_Int = []
    P_Enc = [0 for i in range(n)]

    # Computing P_Int : Intermediate encryption before permutation and after multiplication by inverse of M
    for i in range(d):
        P_Int.append(S[i] - 2 * Point[i])

    P_Int.append(S[d] + MP2)

    for i in T:
        P_Int.append(i)

    for i in v:
        P_Int.append(i)

    #Permutation of the Intermediate Key
    Temp = 0
    for X in P_Int:
        P_Enc[Perm[c]] = X
        Temp += 1

    P_Enc = np.array(P_Enc).reshape(1,-1)
    M = np.array(M)
    M_inv = np.linalg.inv(M)

    P_Enc = np.matmul(P_Enc, M_inv)
    P_Enc = P_Enc.tolist()

    # Returning the encrypted point as a python list
    return P_Enc[0]


# Encryption of the Entire Database
def DatabaseEnc(Database, Key):
    Encrypted_Data = []

    for i in range(m):
        v = [random.random() * 1000 for _ in range(epsilon)]

        P_Enc_i = DatapointEnc(Database, i, Key, v)

        Encrypted_Data.append(P_Enc_i)

    return Encrypted_Data

# It is difficult to send the entire data as once to the cloud server.
# We set up a function to send packets of data across the socket connection
def Send_Data(socket, data, size):
    Total_Sent = 0
    while Total_Sent < len(data):
        Packet = data[Total_Sent:Total_Sent + size]
        Total_Sent += socket.send(Packet)


def Send_Database(Encrypted_Data):
    Data_Owner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Helpful to debug OSError : [Errno 98] Address already in use
    Data_Owner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Data_Owner.bind(ADDR_DO)
    Data_Owner.connect(ADDR_CS)

    print(f"[DATA OWNER] Connected to Cloud Server at {ADDR_CS}")

    # Setting the buffer size at 4096
    Send_Data(Data_Owner, json.dumps(Encrypted_Data).encode(), 4096)

    print(f"[DATA OWNER] Sent Encrypted Data to Cloud Server")
    Data_Owner.close()

    print("[DATA OWNER] Connection with Cloud Server Closed")
    

# *** Interaction with Cloud Server Complete ***

def E_pk(num, N, G):
    num = int(num)
    if num > N:
        raise ValueError("Number too large to encrypt, INVALID QUERY")
    k1 = pow(G, num, (N * N))

    # Random Parameter used for Encryption
    r = np.random.randint(1, N)
    while not GCD(r, N) == 1:
        r = np.random.randint(1, N)
    r = int(r)
    k2 = pow(r, N, N ** 2)

    c_num = (k1 * k2) % (N ** 2)
    return c_num



# Function to furthur encrypt the query received from the query user
def QueryEnc(query, Key):
    if(len(query) != d):
        return False
    
    Perm = Key[3]
    M = Key[0]
    c = len(Key[2])
    B_q = 1 + int(random.random() * 99) # Random paramater used for query encryption
    R_q = [1 + int(random.random() * 99) for i in range(c)]

    A_q = [0 for i in range(n)]

    # Here X = N and Y = G, which are the Paillier Encryption Public Parameters
    X = int(query["PaillierN"])
    Y = int(query["PaillierG"])
    Z = np.array(query["Query"])

    Inverse_Pi = Inverse_Perm(Perm)

    for i in range(n):
        A_q[i] = int(E_pk(0, X, Y))
        
        for j in range(n):
            t = Inverse_Pi[j]
            if t < d:
                phi = int(B_q) * int(M[i][j])
                A_q[i] = int(abs(A_q[i]) * pow(Z[t], phi, (X ** 2)))

            elif t == d:
                phi = int(B_q) * int(M[i][j])
                A_q[i] = A_q[i] * (E_pk(phi, X, Y) % (X ** 2))

            elif t < (d + 1 + c):
                omega = t - d - 1
                phi = int(B_q) * int(M[i][j]) * int((R_q[omega]))
                A_q[i] = A_q[i] * (E_pk(phi, X, Y) % (X ** 2))
             
    return A_q



# This function receives, encryptsthe query from the query user and resolves it as well
def Query_Resolution(Key):
    Data_Owner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Data_Owner.setsockopt(socket.SOL_SOCKEY, socket.SO_REUSEADDR, 1)

    Data_Owner.bind(ADDR_DO)
    Data_Owner.listen()

    print(f"[DATA OWNER] Listening on {ADDR_CS}")

    while True:
        conn, addr = Data_Owner.accept()
        print(f"[DATA OWNER]{addr} connected ...")

        connected = True
        while connected:
            # Convert the received message to a python list
            Message = json.loads(conn.recv(32768).decode())

            A_q = QueryEnc(Message, Key)

            print("[DATA OWNER] A_q Computation Completed")

            conn.sendall(json.dumps(A_q).encode())

            print("[DATA OWNER] Sent Encrypted Query back to the Query User")
            Data_Owner.close()

            connected = False

        print(f"[DATA OWNER] {addr} has disconnected")
        break



#=============================================================================================================
    
Data = GetDatabase()
print("[DATA OWNER] Obtained Database")

Key = PrivateKeyGen()
print("[DATA ONWER] Generated Private Key")

Data_Encrypted = DatabaseEnc(Data, Key)
print("[DATA OWNER] Encrypted Database Using Private Key")

# Sending Data to the Cloud Server
Send_Database(Data_Encrypted)

# Query Resolution
Query_Resolution(Key)
