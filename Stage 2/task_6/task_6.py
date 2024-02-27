'''
# Team ID:          1470
# Theme:            Geo Guide
# Author List:      Parth Jain, Anikesh Kulal, Akash Kolakkal, Keshav Jha
# Filename:         task_6.py
# Functions:        start_server, handle_connections, handle_client, live_feed, main
# Global variables: conn, stop_server, s
'''

#Importing the required libraries

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

# Global variables
conn = None
stop_server = False

# Creating a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Function Name: start_server
# Input: None
# Output: None
# Logic: This function is used to start the server
# Example Call: start_server()

def start_server():
    global conn, stop_server        
    HOST = '192.168.60.163'                                             # The server's hostname or IP address
    PORT = 8002                                                         # The port used by the server

    s.bind((HOST, PORT))

    while not stop_server:                                              # Loop to keep the server running
        s.listen()
        handle_connections()
    s.close()


# Function Name: handle_connections
# Input: None
# Output: None
# Logic: This function is used to handle the connections from the client
# Example Call: handle_connections()

def handle_connections():
    global conn, stop_server
    while not stop_server:          
        conn, addr = s.accept()                                         # Accepting the connection
        threading.Thread(target=handle_client, args=(conn,)).start()    # Creating a new thread to handle the client


# Function Name: handle_client
# Input: conn: The connection object
# Output: None
# Logic: This function is used to handle the client
# Example Call: handle_client(conn)

def handle_client(conn):
    while not stop_server:
        data = conn.recv(1024)                                          # Receiving the data from the client
        if not data:                                 
            break
    conn.close()
    
    
# Function Name: live_feed
# Input: None
# Output: None
# Logic: This function is used to get the live feed from the camera and send the path to the client
# Example Call: live_feed()

def live_feed():
    labels_dict = classify_and_label_events()                           # Getting the labels of the events
    
    string_path, event_list = calculate_path_string(labels_dict)        
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)                            # Creating a video capture object
    cap.set(3, 1920)                                                    # Setting the width of the frame
    cap.set(4, 1080)                                                    # Setting the height of the frame
    cap.set(cv2.CAP_PROP_FPS, 30)                                       # Setting the frame rate
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))       # Setting the codec
    cap.set(cv2.CAP_PROP_AUTO_WB, 0)                                    # Setting the white balance
    cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 1000)                          # Setting the white balance temperature

    file_path = 'output.csv'                                            # Path to the output file
    i = 0
    sent = False                                                        # To check if the data has been sent to the client

    for _ in range(30):
        ret, frame = cap.read()                                         # Reading the frame from the camera

    while True:
        ret, frame = cap.read()                                         
        if not ret:
            break

        if not sent:
            if conn:
                conn.sendall(string_path.encode())
                sent = True

        frame = get_arena(frame)                                        # Getting the arena from the frame
        ArUco_details_dict, ArUco_corners = detect_ArUco_details(frame) # Detecting the ArUco details

        lat, lon = None, None                                           # Initializing the latitude and longitude

        try:
            
            event = event_list[0]                                       # Getting the first event from the event list
            if did_reach(ArUco_details_dict[100][0], event):
                if conn:
                    conn.sendall(b'1')                                  # Sending the data to the client
                event_list.pop(0)
                        
        except:
            pass
            
        try:
            
            center = ArUco_details_dict[100][0]                         # Getting the center of the ArUco marker
            angle = ArUco_details_dict[100][1]                          # Getting the angle of the ArUco marker
            lat, lon = get_lat_lon(center, angle)                       # Getting the latitude and longitude
        except:
            pass

        if lat != None and lon != None:
            with open(file_path, 'w', newline='') as csv_file:

                csv_writer = csv.writer(csv_file)                       # Creating a csv writer object

                data = [                                                # Data to be written in the csv file
                    ['lat', 'lon'],
                    [lat, lon]
                ]

                csv_writer.writerows(data)                              # Writing the data to the csv file

        frame = cv2.resize(frame, (950, 950))                           # Resizing the frame
        cv2.imshow("ArUco Marker Detection", frame)                     
        i = (i % 10) + 1                                                

        if cv2.waitKey(1) & 0xFF == ord('q'):                           # Checking if the user has pressed the 'q' key
            break

    cap.release()                                                       
    cv2.destroyAllWindows()                                             


# Function Name: main
# Input: None
# Output: None
# Logic: This function is used to start the server and the live feed
# Example Call: main()

def main():
    server_thread = threading.Thread(target=start_server)               # Creating a new thread to start the server
    live_feed_thread = threading.Thread(target=live_feed)               # Creating a new thread to get the live feed

    server_thread.start()
    live_feed_thread.start()                                                

    server_thread.join()
    live_feed_thread.join()

if __name__ == '__main__':

    process = Process(target=main)                                      # Creating a new process to run the main function
    process.start()

    while process.is_alive():
        if keyboard.is_pressed('p'):
            process.terminate() 
            break