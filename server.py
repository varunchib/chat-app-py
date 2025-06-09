import socket
import threading
import psycopg2

conn = psycopg2.connect(
    dbname="practise", user="postgres", password="darkangel", host="localhost", port="5432"
)
cur = conn.cursor()

HOST = '127.0.0.1'
PORT = 5000
clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client, addr):
    print(f"[+] New connection from {addr}")
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            username, msg = data.decode().split(":", 1)
            # Save message
            cur.execute("INSERT INTO chat.messages (username, message) VALUES (%s, %s)", (username, msg.strip()))
            conn.commit()
            broadcast(data, client)
        except:
            break

    client.close()
    clients.remove(client)
    print(f"[-] Connection closed: {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f" Server listening on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    start_server()