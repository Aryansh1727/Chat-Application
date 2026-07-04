# Chat-Application
# 💬 Real-Time Python Socket Chat Application

A responsive, feature-rich Python desktop chat application built using **Tkinter** for the UI, **Sockets** for network communication, and **SQLite** for automated message history tracking.

## ✨ Features
* 🌙 **Dynamic Themes:** Smoothly toggle between Light and Dark modes (updates backgrounds, text tints, and insertion cursors).
* 🔍 **Live Keyword Search:** Instantly highlights matching words or phrases across the chat log as you type.
* 📏 **Entry Constraints:** Real-time character monitoring that automatically caps input at a maximum of 250 characters.
* 🗑️ **Chat Screen Clearer:** Clears out old message logs from the active window view with a single click without wiping database backups.
* ⚡ **Anti-Overlapping Layout:** Smart geometry algorithms that automatically calculate screen space to spawn the Server and Client windows side-by-side.

## 🛠️ Project Structure
* `server.py` — The central server script that initializes the network host and manages incoming socket messages.
* `client.py` — The client script that connects directly to the server host.
* `layout.py` — The core graphical layout, theme configurations, widgets, and utility tools.
* `database.py` — Manages the SQLite connection to automatically save and retrieve chat histories.
* `view_db.py` — A developer utility script to print and inspect the logged SQLite database records directly in the terminal.

## 🚀 How to Run

### Method A: Via Terminal
1. Boot up the server backend:
   ```bash
   python server.py
2. Open a separate terminal window and launch the client connection:
   ```bash
   python client.py
3. Enter your unique usernames and start chatting!

### Method B: No Terminal (Windows)
Rename `server.py` and `client.py` to `server.pyw` and `client.pyw` respectively, 
then double-click them to run the app silently without launching a command prompt box.
