import socket
import signal
import sys
import threading
import keyboard

def signal_handler(sig, frame):
    print('Clean-up!')
    cleanup()
    sys.exit(0)

def cleanup():
    s.close()
    print("Cleanup done")

def send_data(direction):
    conn.sendall(str.encode(direction))
    data = conn.recv(1024)
    print(data)

def handle_input():
    while True:
        try:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name.upper()
                if key in ["W", "A", "S", "D", "Q"]:
                    send_data("1" if key == "W" else "2" if key == "S" else "3" if key == "A" else "4" if key == "D" else "5")
        except KeyboardInterrupt:
            break

# Enter the IP address of the laptop after connecting it to the WIFI hotspot
ip = "192.168.1.3"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, 8002))
    s.listen()
    conn, addr = s.accept()

    with conn:
        print(f"Connected by {addr}")

        # Create a thread to handle user input
        input_thread = threading.Thread(target=handle_input)
        input_thread.start()

        # Wait for the input thread to finish
        input_thread.join()

        cleanup()
