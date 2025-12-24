



import socket 
import threading 
import queue
from datetime import datetime 

messages = queue.Queue()
clients = [] 


ip = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((ip, 6666))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode())
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:

                    if message.decode().startswith("SIGNUP_TAG"):
                        name = message.decode()[message.decode().index(":")+1:].strip()
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        server.sendto(f"[{timestamp}] {name} joined!".encode(), client)
                    elif message.decode().startswith("TYPING:"):
                        # Typing indicator
                        typing_user = message.decode()[message.decode().index(":")+1:].strip()
                        # Broadcast typing indicator to all other clients (not the sender)
                        for other_client in clients:
                            if other_client != addr:
                                server.sendto(f"{typing_user} is typing...".encode(), other_client)
                    else:
                        decoded_msg = message.decode()
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        # Add timestamp to the message
                        if ":" in decoded_msg:
                            parts = decoded_msg.split(":", 1)
                            username = parts[0]
                            msg_text = parts[1]
                            timestamped_msg = f"[{timestamp}] {username}:{msg_text}"
                        else:
                            timestamped_msg = f"[{timestamp}] {decoded_msg}"
                        server.sendto(timestamped_msg.encode(), client)
                except:
                    clients.remove(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()


        # Send the actual message
        client.sendto(f"{name}: {message}".encode(), (ip, 6666))

