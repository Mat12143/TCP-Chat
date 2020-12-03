import socket
import threading
from termcolor import colored
from getpass import getpass

stop_thread = False
exit_volontario = False

# Choosing Nickname
nickname = input("Choose your nickname: ")

if nickname.lower() == "admin":
    password = getpass("Inserisci la password di amministratore: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.2.103', 55555))

# Listening to Server and Sending Nickname
def receive():

    global stop_thread, exit_volontario

    while stop_thread == False:

        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))

                next_message = client.recv(1024).decode("utf-8")

                if next_message == "PASS":
                    client.send(password.encode("utf-8"))

                    if client.recv(1024).decode("utf-8") == "NONACCETTO":
                        print("Password errata!")
                        client.send("EXIT".encode("utf-8"))
                        stop_thread = True

            elif message == "Connesso al server!":
                print(colored((message), "yellow"))

            elif "è atterrato!" in message or "è uscito!" in message:
                if not nickname in message:
                    print(colored(message, "yellow"))

            elif message == "Un ADMIN è atterrato nella chat!":

                print(colored(message, "yellow"))

            else:
                print(message)
        except:
            if exit_volontario == False:
                print("Il server non è più Online! Esco")
                stop_thread = True

# Sending Messages To Server
def write():
    global stop_thread

    while stop_thread == False:

        message = input("")

        if message == "exit":

            print("Uscito!")

            client.send("EXIT".encode("utf-8"))

            exit_volontario = True
            stop_thread = True
        
        message = f"{nickname}: {message}"

        client.send(message.encode('utf-8'))


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()