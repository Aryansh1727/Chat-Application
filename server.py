import socket
import threading
import time
from datetime import datetime
from layout import create_window, append_message, get_username, load_history_into_ui
from database import init_db, save_message

init_db()
MY_NAME = get_username("Server")
CLIENT_NAME = "Client"

HOST = "127.0.0.1"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for client...")
conn, addr = server.accept()

# Handshake usernames over the network socket
conn.send(MY_NAME.encode())
CLIENT_NAME = conn.recv(1024).decode()

# Typing reset clock tracking variable
last_typing_time = 0

def send_typing_signal():
    global last_typing_time
    current_time = time.time()
    if current_time - last_typing_time > 2: # Limit typing signal spamming
        try:
            conn.send("__TYPING__".encode())
            last_typing_time = current_time
        except:
            pass

root, chat_area, entry, send_btn, typing_label = create_window("Server", MY_NAME, send_typing_signal)

# Load existing history seamlessly on launch
load_history_into_ui(chat_area, MY_NAME)

def clear_typing_status():
    time.sleep(2)
    typing_label.config(text="")

def receive():
    global CLIENT_NAME
    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg == "__TYPING__":
                typing_label.config(text=f"✍️ {CLIENT_NAME} is typing...")
                threading.Thread(target=clear_typing_status, daemon=True).start()
            elif msg:
                current_time = datetime.now().strftime("%I:%M %p")
                append_message(chat_area, CLIENT_NAME, msg, "left", current_time, is_self=False)
        except:
            break

def send(event=None):
    msg = entry.get().strip()
    if msg:
        try:
            conn.send(msg.encode())
            current_time = datetime.now().strftime("%I:%M %p")
            append_message(chat_area, "You", msg, "right", current_time, is_self=True)
            save_message(MY_NAME, msg)
            entry.delete(0, "end")
        except:
            pass

send_btn.config(command=send)
root.bind("<Return>", send)

threading.Thread(target=receive, daemon=True).start()
root.mainloop()

conn.close()
server.close()