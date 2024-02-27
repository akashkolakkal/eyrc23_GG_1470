'''
# Team ID:          1470
# Theme:            Geo Guide
# Author List:      Parth Jain, Anikesh Kulal, Akash Kolakkal, Keshav Jha
# Filename:         utilities.py
# Functions:        calculate_distance, get_center, get_angle, detect_ArUco_details, did_reach, get_arena
# Global variables: None
'''

import cv2
import numpy as np
import math
from cv2 import aruco
import matplotlib.pyplot as plt

def calculate_distance(p1, p2):
    '''
    * Function Name:    calculate_distance
    * Input:            p1 -> The first point, p2 -> The second point
    * Output:           The distance between the two points
    * Logic:            This function is used to calculate the distance between the two points
    * Example Call:     calculate_distance((1, 2), (3, 4))
    '''
    # Here we used the distance formula to calculate the distance between the two points
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)       

def get_center(corners):
    '''
    * Function Name:    get_center
    * Input:            corners -> The corners of the ArUco marker
    * Output:           The center of the ArUco marker
    * Logic:            This function is used to get the center of the ArUco marker
    * Example Call:     get_center([[1, 2], [3, 4], [5, 6], [7, 8]])
    '''
    
    x = 0                                                                    # Initializing the x-coordinate of the center
    y = 0                                                                    # Initializing the y-coordinate of the center
    
    # Loop to calculate the sum of the x and y coordinates of the corners
    for i in corners:
        x += i[0]
        y += i[1]

    x = x/len(corners)                                                       # Calculating the x-coordinate of the center
    y = y/len(corners)                                                       # Calculating the y-coordinate of the center

    return [int(x), int(y)]                                 

def get_angle(center, corner):
    '''
    * Function Name:    get_angle
    * Input:            center -> The center of the ArUco marker, corner -> The corner of the ArUco marker
    * Output:           The angle of the ArUco marker
    * Logic:            This function is used to get the angle of the ArUco marker
    * Example Call:     get_angle([1, 2], [3, 4])
    '''
    x1, y1 = center                                                          # Getting the x and y coordinates of the center
    x2, y2 = corner                                                          # Getting the x and y coordinates of the corner
    
    # Calculating the angle of the ArUco marker
    angle = math.degrees(math.atan2(x2 - x1, y2 - y1))      
    return int(angle)

def detect_ArUco_details(image):
    '''
    * Function Name:    detect_ArUco_details
    * Input:            image -> The image in which the ArUco markers are to be detected
    * Output:           ArUco_details_dict -> The dictionary containing the details of the ArUco markers, ArUco_corners -> The corners of the ArUco markers
    * Logic:            This function is used to detect the ArUco markers and get their details
    * Example Call:     detect_ArUco_details(image)
    '''
    ArUco_details_dict = {}                                             # Initializing the dictionary to store the details of the ArUco markers
    ArUco_corners = {}                                                  # Initializing the dictionary to store the corners of the ArUco markers

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)           # Getting the aruco dictionary
    parameters = aruco.DetectorParameters()                                  # Getting the aruco detector parameters

    detector = aruco.ArucoDetector(aruco_dict, parameters)                   # Creating an aruco detector object

    corners, ids, rejected_img_points = detector.detectMarkers(image)        # Detecting the ArUco markers

    # Loop to get the details of the ArUco markers
    for i in range(len(ids)):
        ArUco_corners[int(ids[i][0])] = corners[i][0]

        center = get_center(ArUco_corners[ids[i][0]])               

        ArUco_details_dict[int(ids[i][0])] = [center, get_angle(            
            ArUco_corners[ids[i][0]][0], ArUco_corners[ids[i][0]][3])]          

    # Returning the dictionary containing the details of the ArUco markers and the corners of the ArUco markers
    return ArUco_details_dict, ArUco_corners                        

def did_reach(center, event):
    '''
    * Function Name:    did_reach
    * Input:            center -> The center of the ArUco marker, event -> The event to be reached
    * Output:           True if the bot has reached the event, False otherwise
    * Logic:            This function is used to check if the bot has reached the event
    * Example Call:     did_reach([1, 2], 'A')
    '''
    events = {                                      # Dictionary to store the coordinates of the events
        "A": (300, 900),
        "B": (750, 670),
        "C": (750, 470),
        "D": (300, 475),
        "E": (300, 130)
    }
    
    # Checking if the bot's distance from the event is less than 60 pixels, then return true else return false
    if math.sqrt((center[0] - events[event][0])**2 + (center[1] - events[event][1])**2) <= 60:
        return True
    return False

def get_arena(img):  
    '''
    * Function Name:    get_arena
    * Input:            img -> The image of the arena
    * Output:           The top-down view of the 1080x1080 square view of the arena
    * Logic:            This function is used to get the top-down view of the 1080x1080 square view of the arena
    * Example Call:     get_arena(img)
    '''  
    # The actual and should be coordinates of the arena
    # The actual coordinates are mannually extracted from the image taken by the camera
    #
    # We had tried to use the ArUco markers to get the perspective transform matrix, 
    # but it was giving us inconsistent results due tho the change in angle of the overhead camera, 
    # so we decided to mannually extract the corners of the arena
    actual = np.float32([[548, 22], [1568, 20], [1585, 1059], [523, 1039]])
    should_be = np.float32([[0, 0], [1080, 0], [1080, 1080], [0, 1080]])

    pers_M = cv2.getPerspectiveTransform(actual, should_be)         # Getting the perspective transform matrix
    rows, cols, ch = img.shape                                      # Getting the rows, columns, and channels of the image

    img = cv2.warpPerspective(img, pers_M, (cols, rows))            # Warping the image to get the top-down view of the arena

    # Returning the top-down view of the 1080x1080 square view of the arena
    return img[:, :1080]


def helper_arena():
    '''
    * Function Name:    helper_arena
    * Input:            None
    * Output:           None
    * Logic:            This is a helper function that we are using to mannually extract the corner coordinates of the arena
    *                   NOT used in the main code, only used to get the coordinates of the arena
    * Example Call:     helper_arena()
    '''

    # Capturing the image of the arena
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    for _ in range(30):
        ret, frame = cap.read()

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame.")

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    fig, ax = plt.subplots()
    ax.imshow(frame)

    plt.axis("off")
    plt.show()

    # Manually extracting the coordinates of the arena here, which is then copied to the get_arena function
    actual = np.float32([[548, 22], [1568, 20], [1585, 1059], [523, 1039]])


if __name__ == "__main__":
    # Only used to get the coordinates of the arena, not to be used in the main code
    helper_arena()
