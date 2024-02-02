import numpy as np
import cv2
import matplotlib.pyplot as plt
import csv
from utilities import detect_ArUco_details, get_closest_id, get_arena, mark_ArUco_image, did_reach
from task_4a import return_labels_dict
from pathfinder import calculate_path
import socket
import sys
import threading
import keyboard


conn = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start_server():
    global conn
    # Set the server address and port
    HOST = '192.168.102.163'  # The server's hostname or IP address
    PORT = 8002        # The port used by the server

    # Bind the socket to address and port
    s.bind((HOST, PORT))

    # Listen for incoming connections
    s.listen()

    print(f"Server started at {HOST}:{PORT}")
    handle_connections()


def handle_connections():
    global conn
    while True:
        # Wait for a connection
        conn, addr = s.accept()
        print('Connected by', addr)
        conn.sendall(b'Connection established. Hello from the server!')

        threading.Thread(target=handle_client, args=(conn,)).start()


def handle_client(conn):
    while True:
        # Receive data from the client
        data = conn.recv(1024)

        # If no data is received, break the loop
        if not data:
            break

        print('Received from client:', data.decode())
        
        # conn.sendall(b'1')
        # print('Sending to client: 1')
        # # Here you can add your did_reach() condition
        # if keyboard.read_event('w'):
        #     # Send data to the client
        #     key = keyboard.read_event('w')
        #     if key:
        #         print('Sending to client: 1')
        #         conn.sendall(b'1')
            

    # Close the connectionw
    conn.close()


def path_for_bot():
    labels_dict = return_labels_dict()
    priority_list = ['fire', 'destroyed_buildings',
                     'human_aid_rehabilitation', 'military_vehicles', 'combat']
    event_priority = []
    path = ["S"]

    temp = 0

    for label in labels_dict.values():
        if label != 'None':

            priority = priority_list.index(label)
            if priority in event_priority:
                temp += 1

            event_priority.append(priority + temp)
        else:
            event_priority.append(1000)

    print(event_priority)


    while (len(event_priority) > 0):
        min_index = event_priority.index(min(event_priority))
        if event_priority[min_index] != 1000:
            path.append(chr(min_index + 65))
        event_priority.pop(min_index)

    path.append("S")

    complete_path = calculate_path(path)

    string_path = "p"
    for i in complete_path:
        string_path += i
    
    if conn:
        conn.sendall(string_path.encode())
        print('Sending to client:', string_path)

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    file_path = 'task_4b.csv'

    # for live camera feed

    i = 0
    path.pop(-1)
    path.pop(0)


    for _ in range(30):
        ret, frame = cap.read()
    
    #plot frame using pyplot
    frame = get_arena(frame)
    plt.imshow(frame)
    plt.show()


    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame.")
            break

        frame = get_arena(frame)
        ArUco_details_dict, ArUco_corners = detect_ArUco_details(frame)
        # frame = mark_ArUco_image(frame, ArUco_details_dict, ArUco_corners)

        lat, lon = None, None

        
        
        try:
            if (i % 10 == 0):
                lat, lon = get_closest_id(ArUco_details_dict)

            event = path[0]
            if did_reach(ArUco_details_dict[100][0], event):
                if conn:
                    print('Sending to client: 1')
                    conn.sendall(b'1')
                path.pop(0)

        except:
            pass

        if lat != None and lon != None:
            with open(file_path, 'w', newline='') as csv_file:

                csv_writer = csv.writer(csv_file)

                data = [
                    ['lat', 'lon'],
                    [lat, lon]
                ]

                csv_writer.writerows(data)

        frame = cv2.resize(frame, (950, 950))
        cv2.imshow("ArUco Marker Detection", frame)
        i += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    # SERVER

    # start_server()

    # ['destroed', 'fire', 'None', 'military', 'combat']
    thread1 = threading.Thread(target=start_server)
    thread2 = threading.Thread(target=path_for_bot)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()