# Multi-Threaded Echo Server

This project implements a basic multi-threaded echo server in Python. The server listens for incoming client connections and echoes back any messages it receives. 

In this assignment, I created clients on separate threads to simulate multiple clients connecting to the server simultaneously. By using multi-threading on the client side, I could generate multiple requests concurrently, allowing me to test the server's ability to handle multiple incoming connections at the same time. This approach demonstrates the server's multi-threaded nature, as each client connection is handled in a separate thread on the server.


## How to Run

1. **Start the Server**:
   - Open a terminal and run the following command:
     ```bash
     python server.py
     ```
   - This starts the server on `127.0.0.1:3000` and begins listening for incoming client connections.

2. **Start the Client**:
   - Open another terminal and run the following command:
     ```bash
     python client.py
     ```
   - This script will create multiple client threads, each sending a unique message to the server.

### Example Output

**Server Output**:

```
[INFO]          Server Listening on 127.0.0.1:3000
[INFO]          Client Connected : 127.0.0.1:53635
[INFO]          Message received from client : Hello from client 2
[INFO]          Client Connected : 127.0.0.1:53636
[INFO]          Message received from client : Hello from client 1
[INFO]          Client Connected : 127.0.0.1:53637
[INFO]          Message received from client : Hello from client 3
[INFO]          Client Connected : 127.0.0.1:53638
[INFO]          Message received from client : Hello from client 4
[INFO]          Client Connected : 127.0.0.1:53639
[INFO]          Message received from client : Hello from client 5
```

**Client Output**:

```
[INFO]          Client 1 connected to server
[INFO]          Sending message Hello from client 1
[INFO]          Client 2 connected to server
[INFO]          Sending message Hello from client 2
[INFO]          Client 3 connected to server
[INFO]          Sending message Hello from client 3
[INFO]          Client 5 connected to server
[INFO]          Sending message Hello from client 5
[INFO]          Client 4 connected to server
[INFO]          Sending message Hello from client 4
[INFO]          Message Received from server: Hello from client 2
[INFO]          Message Received from server: Hello from client 1
[INFO]          Message Received from server: Hello from client 3
[INFO]          Message Received from server: Hello from client 4
[INFO]          Message Received from server: Hello from client 5
```