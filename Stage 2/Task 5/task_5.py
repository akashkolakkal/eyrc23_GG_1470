'''
# Team ID:          1470
# Theme:            Geo Guide
# Author List:      Parth Jain, Akash Kolakkal, Anikesh Kulal, Keshav Jha
# Filename:         task_5.py
# Functions:        start_server, handle_connections, handle_client, calculate_path_string, path_for_bot
# Global variables: conn, stop_server, s
'''

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
stop_server = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def start_server():
    global conn, stop_server
    HOST = '192.168.166.228'  # The server's hostname or IP address
    PORT = 8002        # The port used by the server

    s.bind((HOST, PORT))

    while not stop_server:
        s.listen()

        print(f"Server started at {HOST}:{PORT}")

        handle_connections()

    s.close()


def handle_connections():
    global conn, stop_server

    while not stop_server:
        conn, addr = s.accept()
        print('Connected by', addr)

        threading.Thread(target=handle_client, args=(conn,)).start()


def handle_client(conn):
    while not stop_server:
        data = conn.recv(1024)
        if not data:
            break
        print('Received from client:', data.decode())
    conn.close()


def calculate_path_string(labels_dict):
    priority_list = ['Fire', 'Destroyed Buildings',
                     'Humanitarian Aid Rehabilitation', 'Military Vehicles', 'Combat']
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

    while (min(event_priority) != 1000):
        min_index = event_priority.index(min(event_priority))

        if event_priority[min_index] != 1000:
            path.append(chr(min_index + 65))
            event_priority[min_index] = 1000

    path.append("S")
    print(path)

    complete_path = calculate_path(path)

    return complete_path, path[1:-1]


def path_for_bot():
    labels_dict = return_labels_dict()
    string_path, event_list = calculate_path_string(labels_dict)

    cap = cv2.VideoCapture(2 , cv2.CAP_DSHOW)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    # cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    # cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 5000)


    file_path = 'task_4b.csv'
    i = 0
    sent = False

    for _ in range(30):
        ret, frame = cap.read()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame.")
            break

        if not sent:
            if conn:
                conn.sendall(string_path.encode())
                print('Sending to client:', string_path)
                sent = True

        frame = get_arena(frame)
        ArUco_details_dict, ArUco_corners = detect_ArUco_details(frame)
        # frame = mark_ArUco_image(frame, ArUco_details_dict, ArUco_corners)

        lat, lon = None, None

        try:
            
            event = event_list[0]
            if did_reach(ArUco_details_dict[100][0], event):
                if conn:
                    print('Sending to client: 1')
                    conn.sendall(b'1')
                event_list.pop(0)
                        


        except:
            pass
            
        try:
            if (i % 10 == 0):
                lat, lon = get_closest_id(ArUco_details_dict)
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

        frame = cv2.resize(frame, (850, 850))
        cv2.imshow("ArUco Marker Detection", frame)
        i = (i % 10) + 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
    cap.set(3, 1920)
    cap.set(4, 1080)
    # cap.set(cv2.CAP_PROP_FPS, 30)
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    # cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    # cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 5000)


    while True:
        ret, frame = cap.read()
        frame = get_arena(frame)

        if not ret:
            print("Failed to capture frame.")
            break
        
        frame = cv2.resize(frame, (850, 850))
        cv2.imshow("Live Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # ['destroed', 'fire', 'None', 'military', 'combat']
    thread1 = threading.Thread(target=start_server)
    thread2 = threading.Thread(target=path_for_bot)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()
