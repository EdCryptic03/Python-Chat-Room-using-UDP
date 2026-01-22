import socket 
import threading 
import random
import time
from datetime import datetime 
random_socket = random.randint(8000, 9000)
ip = socket.gethostbyname(socket.gethostname())
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((ip, random_socket))

name = input("Nickname: ")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            decoded_msg = message.decode()
            if not decoded_msg.startswith("["):
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] {decoded_msg}")
            else:
                print(decoded_msg)
        except:
            pass

t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG: {name}".encode(), (ip, 6666))

while True:
    message = input("")
    if message == '!q':
        exit()
    else:
        client.sendto(f"TYPING: {name}".encode(), (ip, 6666))
        time.sleep(0.1)
        client.sendto(f"{name}: {message}".encode(), (ip, 6666))

