import cv2
import numpy as np
import math
from cv2 import aruco

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

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

def did_reach(center, event):
    events = {
        "A": (300, 900),
        "B": (750, 670),
        "C": (750, 470),
        "D": (300, 475),
        "E": (300, 130)
    }

    if math.sqrt((center[0] - events[event][0])**2 + (center[1] - events[event][1])**2) <= 60:
        return True
    return False


def get_arena(img):    
    
    actual = np.float32([[548, 22], [1568, 20], [1585, 1059], [523, 1039]])
    should_be = np.float32([[0, 0], [1080, 0], [1080, 1080], [0, 1080]])

    pers_M = cv2.getPerspectiveTransform(actual, should_be)
    rows, cols, ch = img.shape

    img = cv2.warpPerspective(img, pers_M, (cols, rows))

    return img[:, :1080]


