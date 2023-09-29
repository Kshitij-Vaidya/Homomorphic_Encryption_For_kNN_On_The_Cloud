The following codes are to be executed in order on the terminal window to build and run the dockerfile:
1. docker build -t <image-name> .

2. docker run -t -i -v factors-db:/app/factors-db -v /tmp/data:/app/data -p 65433:65433 <image_name>

This will start the SERVER

3. Run the Data Owner and Query User on separate terminal windows using the commands:
   python3 data_owner.py
   python3 query_user.py

4. The factorisation is appended to a file in factors-db: named factorisation.txt
   This can be checked by the command:
   docker ps -a    # This returns the container ID
   docker exec <container-ID> cat factors-db:/factorisation.txt
   

Ensure that multiple instances of the Docker container are not running, this may result it connection errors between the query user and the server
