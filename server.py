



import socket 
import threading 
import queue
from datetime import datetime 

""" Firstly, I created an empty list for the clients.
 Secondly, I created receive and broadcast functions to receive messages from the clients to the server 
 and then using the broadcast functions to broadcast the message to all the other clients connected to the server.

 Finally, I used threaing to avoid collapsing of many clients joining the server and eventually letting the server crash. Threading allowed many clients to join the server simultaneously.
"""

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
                 
                        typing_user = message.decode()[message.decode().index(":")+1:].strip()
              
                        for other_client in clients:
                            if other_client != addr:
                                server.sendto(f"{typing_user} is typing...".encode(), other_client)
                    else:
                        decoded_msg = message.decode()
                        timestamp = datetime.now().strftime("%H:%M:%S")
                  
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


        client.sendto(f"{name}: {message}".encode(), (ip, 6666))


