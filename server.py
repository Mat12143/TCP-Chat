import socket
import threading, json
from termcolor import colored

host = '127.0.0.1'
port = 55555

banned = {}

users = {}

def apri_file():

    global banned

    with open("banned.json", "r") as f:
        banned = json.load(f)

def salva_file():

    global banned

    with open("banned.json", "w") as f:
        json.dump(banned, f)

apri_file()

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in users.keys():
        client.send(message)

# Handling Messages From Clients
def handle(client):

    global users

    while True:
        try:
            # Broadcasting Messages
            try:
                message = client.recv(1024)
            except:
                print(colored("Errore", "red"))

            if message.decode("utf-8") == "EXIT":
                    
                broadcast('{} è uscito!'.format(users[client]).encode('utf-8'))
                del(users[client])
                break

            broadcast(message)
        except:

            broadcast('{} è uscito!'.format(users[client]).encode('utf-8'))
            del(users[client])
            break

# Receiving / Listening Function
def receive():

    global banned

    while True:
        # Accept Connection
        client, address = server.accept()

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))

        nickname = client.recv(1024).decode('utf-8')

        if nickname.lower() == "admin":
            client.send("PASS".encode("utf-8"))

            password = client.recv(1024).decode("utf-8")

            if password != "securepass":
                client.send("NONACCETTO".encode("utf-8"))
                client.close()
                continue
                
            else:
                broadcast("Un ADMIN è atterrato nella chat!".encode("utf-8"))
                client.send("")

        elif nickname in banned:

            client.send("ERROR-BAN".encode("utf-8"))
            client.close()
            continue
            
        elif str(nickname) in users.values():
            client.send("ERROR-NICK".encode("utf-8"))
            client.close()
            continue

        users[client] = str(nickname)

        print(f"{nickname} è atterrato!")

        if nickname != "admin":
            broadcast(f"{nickname} è atterrato!".encode("utf-8"))

        client.send("Connesso al server!".encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("PRONTO!")
receive()