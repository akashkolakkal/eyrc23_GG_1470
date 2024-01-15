import numpy as np
import cv2
from cv2 import aruco
import math
import matplotlib.pyplot as plt
import csv

def get_center(corners):
    x = 0
    y = 0

    for i in corners:
        x += i[0]
        y += i[1]

    x = x/len(corners)
    y = y/len(corners)

    return [int(x), int(y)]

def get_angle(center, corner):
    x1, y1 = center
    x2, y2 = corner
    angle = math.degrees(math.atan2(x2 - x1, y2 - y1))
    return int(angle)

def detect_ArUco_details(image):
    ArUco_details_dict = {}
    ArUco_corners = {}

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    parameters = aruco.DetectorParameters()

    detector = aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, rejected_img_points = detector.detectMarkers(image)

    for i in range(len(ids)):
        ArUco_corners[int(ids[i][0])] = corners[i][0]

        center = get_center(ArUco_corners[ids[i][0]])

        ArUco_details_dict[int(ids[i][0])] = [center, get_angle(
            ArUco_corners[ids[i][0]][0], ArUco_corners[ids[i][0]][3])]

    return ArUco_details_dict, ArUco_corners

def get_closest_id(ArUco_details_dict):
    closest_dist = 10000000
    closest_id = 42

    try:
        center = ArUco_details_dict[1][0]

        csv_file = open('lat_long.csv', 'r')

        csv_reader = csv.reader(csv_file)

        for id, details in ArUco_details_dict.items():
            dist = math.sqrt((details[0][0] - center[0])**2 + (details[0][1] - center[1])**2)
            if dist < closest_dist and id != 1:
                closest_dist = dist
                closest_id = id
        
        
        for row in csv_reader:
            try:
                if int(row[0]) == int(closest_id):
                    csv_file.close()
                    return row[1], row[2]
            except:
                pass
        csv_file.close()
            
    except:
        print("ArUco marker 1 not detected.")

    return None, None

def get_arena(img):
    actual = np.float32([[396, 6], [1385, 77], [1392, 1065], [313, 1063]])
    should_be = np.float32([[0, 0], [1080, 0], [1080, 1080], [0, 1080]])

    pers_M = cv2.getPerspectiveTransform(actual, should_be)
    rows, cols, ch = img.shape

    img = cv2.warpPerspective(img, pers_M, (cols, rows))

    return img[:, :1080]


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(3, 1920)
cap.set(4, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))


file_path = 'task_4b.csv'

i = 0
for _ in range(30):
    ret, frame = cap.read()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame.")
        break

    
    frame = get_arena(frame)
    ArUco_details_dict, ArUco_corners = detect_ArUco_details(frame)

    lat, lon = None, None

    if (i%10 == 0):
        lat, lon = get_closest_id(ArUco_details_dict)

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

    i = (i + 1) % 10

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()