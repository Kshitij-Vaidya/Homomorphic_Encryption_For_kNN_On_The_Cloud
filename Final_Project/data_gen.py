import random

d = 50 # dimensions of each point in the database

m = 10000 # number of points in the database

path = "/Users/kshitijvaidya/Desktop/VirtualEnvironment/SoC_Project/Final_Project/database.txt"

for i in range(10000):
    data = []
    for j in range(50):
        data.append(random.randint(-10000, 10000))

    with open(path, "a") as file:
        file.write(str(data) + "\n")
