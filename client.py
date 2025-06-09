import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

username = input("Enter your username: ")

def receive(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            print(message)
        except:
            print("Disconnected from server")
            sock.close()
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

threading.Thread(target=receive, args=(client,), daemon=True).start()

while True:
    msg = input()
    if msg.lower() == "exit":
        client.close()
        break
    full_msg = f"{username}: {msg}"
    client.send(full_msg.encode())