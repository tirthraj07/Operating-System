import socket
import threading

HOST = '127.0.0.1'
PORT = 8000


def handle_client(client_socket:socket.socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Message Received from client : {data.decode()}")
        client_socket.send(data)
    client_socket.close()    

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server Listening on {HOST}:{PORT}")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f'Accepted connection from {addr[0]}:{addr[1]}')
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
        except:
            break

if __name__ == '__main__':
    main()