import socket
import keyboard
import threading

conn = None
stop_server = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def start_server():
    global conn, stop_server

    HOST = '192.168.166.163'  # The server's hostname or IP address
    PORT = 8002        # The port used by the server

    s.bind((HOST, PORT))

    while not stop_server:
        s.listen()

        print(f"Server started at {HOST}:{PORT}")

        if stop_server:
            break

        handle_connections()

    print("Server stopped")
    s.close()


def handle_connections():
    global conn, stop_server

    while not stop_server:
        conn, addr = s.accept()
        print('Connected by', addr)

        if stop_server:
            break

        threading.Thread(target=handle_client, args=(conn,)).start()


def handle_client(conn):
    global stop_server

    while not stop_server:
        data = conn.recv(1024)

        if not data or stop_server:
            break

        if keyboard.is_pressed('q'):
            stop_server = True
            break

        print('Received from client:', data.decode())

    conn.close()


def instructions():
    path = "FFFRRRBRRRLE"
    sent = False
    while (not sent):
        if conn:
            conn.sendall(path.encode())
            print('Sending to client:', path)
            sent = True

    while True:
        if keyboard.read_event('w'):
            conn.sendall(b'1')
            print('Sending to client: 1')


if __name__ == '__main__':
    server_thread = threading.Thread(target=start_server)
    instructions_thread = threading.Thread(target=instructions)

    server_thread.start()
    instructions_thread.start()
