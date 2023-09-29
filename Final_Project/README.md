# Implementation of Secure k-NN Query over the Cloud with Key Security and Query Controllability

## Parameter Ranges and Values Chosen : 
1. **c** is a random integer in the range (1,10)
2. **epsilon** is a random integer in the range (1,10)
3. **v** is an **epsilon** dimensional vector with each entry being a floating point number
4. **M** is an invertible matrix have entries in the range (1,10) - used for encryption
5. Negative Number Handling : To avoid dealing with negative numbers, they are converted to a number between 10000 and 20000 by adding 10000 to their absolute value. This does not affect Euclidean Distance which is the main parameter governing k nearest neighbours.

## Runtime Instructions

The codes are run in the following order :
<br>cloud_server.py -> data_owner.py -> query_user.py

1. Setting up the Cloud Server in a Docker Container. Open the terminal window in the "Final_Project" directory and run the following commands in sequence:
  <br>*docker build -t cloud-server .*
  <br>*docker run -p 65433:65433 cloud-server*
2. Open two separate *SageMath* terminals in the same directory
3. Run the file *data_owner.py* in one of the terminals
   <br>load("data_owner.py")
4. Run the *query_user.py* file in the second terminal window using the command :
   <br> load("query_user.py")

## Additional Comments
The following parts of the code can be changed by the user :
1. Query : I have chosen a test query that is the first line of the data base. This query can be arbitrarily chosen or randomly generated
2. K : K is 1 by default but can be chosen as any value upto 10000
3. The database itself can be changed. This database can be manually created or I have added a python file *data_gen.py* that can create a randomly generated Database in the *database.txt* file. Be sure to erase the previous database.
