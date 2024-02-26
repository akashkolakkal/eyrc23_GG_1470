import numpy as np
import cv2
import matplotlib.pyplot as plt
import csv
from utilities import detect_ArUco_details, get_closest_id, get_arena, mark_ArUco_image, did_reach
from task_4a import classify_and_label_events
from pathfinder import calculate_path
import socket
from live_tracking import get_lat_lon
import threading
import keyboard
from multiprocessing import Process
from pathfinder import calculate_path_string 

conn = None
stop_server = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def start_server():
    global conn, stop_server
    HOST = '192.168.60.163'  # The server's hostname or IP address
    PORT = 8002        # The port used by the server

    s.bind((HOST, PORT))

    while not stop_server:
        s.listen()

        # print(f"Server started at {HOST}:{PORT}")

        handle_connections()

    s.close()

def handle_connections():
    global conn, stop_server

    while not stop_server:
        conn, addr = s.accept()
        # print('Connected by', addr)

        threading.Thread(target=handle_client, args=(conn,)).start()

def handle_client(conn):
    while not stop_server:
        data = conn.recv(1024)
        if not data:
            break
        # print('Received from client:', data.decode())
    conn.close()

def live_feed():
    labels_dict = classify_and_label_events()
    string_path, event_list = calculate_path_string(labels_dict)

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 1000)

    file_path = 'output.csv'
    i = 0
    sent = False

    for _ in range(30):
        ret, frame = cap.read()

    while True:
        ret, frame = cap.read()

        if not ret:
            # print("Failed to capture frame.")
            break

        if not sent:
            if conn:
                conn.sendall(string_path.encode())
                # print('Sending to client:', string_path)
                sent = True

        frame = get_arena(frame)
        ArUco_details_dict, ArUco_corners = detect_ArUco_details(frame)
        # frame = mark_ArUco_image(frame, ArUco_details_dict, ArUco_corners)

        lat, lon = None, None

        try:
            
            event = event_list[0]
            if did_reach(ArUco_details_dict[100][0], event):
                if conn:
                    # print('Sending to client: 1')
                    conn.sendall(b'1')
                event_list.pop(0)
                        
        except:
            pass
            
        try:
            # if (i % 10 == 0):
                # lat, lon = get_closest_id(ArUco_details_dict)
            center = ArUco_details_dict[100][0]
            angle = ArUco_details_dict[100][1]
            lat, lon = get_lat_lon(center, angle)
        except:
            # print("Error in getting lat and lon.")
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
        i = (i % 10) + 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    server_thread = threading.Thread(target=start_server)
    live_feed_thread = threading.Thread(target=live_feed)

    server_thread.start()
    live_feed_thread.start()

    server_thread.join()
    live_feed_thread.join()

if __name__ == '__main__':

    process = Process(target=main)
    process.start()

    while process.is_alive():
        if keyboard.is_pressed('p'):
            process.terminate()
            break