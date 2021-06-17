import socket
import threading
import pickle

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

clients = []
usernames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            username = usernames[index]
            broadcast(F'{username} left the chat'.encode(FORMAT))
            usernames.remove(username)
            client.close()
            break


def receive():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}')

        client.send('NICK'.encode(FORMAT))
        username = client.recv(1024).decode(FORMAT)
        usernames.append(username)
        clients.append(client)       

        broadcast('USERS'.encode(FORMAT))
        connectedUsers = pickle.dumps(usernames)
        broadcast(connectedUsers)  

        print(f'username of client is {username}')
        # broadcast(f'{username} joined the class'.encode(FORMAT))
        # client.send(f"connected to the server".encode(FORMAT))      

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("[STARTING] server is starting...")
receive()
