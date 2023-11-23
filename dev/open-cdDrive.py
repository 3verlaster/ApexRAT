from subprocess import Popen

command = r'powershell.exe -ExecutionPolicy RemoteSigned -Command "$wmp = New-Object -ComObject WMPlayer.OCX; $cdrom = $wmp.cdromCollection.Item(0); $cdrom.eject()"'

Popen(command, shell=True)
