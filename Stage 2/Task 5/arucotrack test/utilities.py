import cv2
import numpy as np
import math
from cv2 import aruco
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
        center = ArUco_details_dict[100][0]

        csv_file = open('lat_long.csv', 'r')

        csv_reader = csv.reader(csv_file)

        for id, details in ArUco_details_dict.items():
            dist = math.sqrt((details[0][0] - center[0])
                             ** 2 + (details[0][1] - center[1])**2)
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


def did_reach(center, event):
    events = {
        "A": (300, 130),
        "B": (750, 670),
        "C": (750, 470),
        "D": (270, 440),
        "E": (300, 130)
    }

    if math.sqrt((center[0] - events[event][0])**2 + (center[1] - events[event][1])**2) <= 80:
        return True
    return False


def get_arena(img):    
    
    actual = np.float32([[777, 0], [1778, 21], [1794, 1019], [761, 1030]])
    should_be = np.float32([[0, 0], [1080, 0], [1080, 1080], [0, 1080]])

    img = cv2.rotate(img, cv2.ROTATE_180)

    pers_M = cv2.getPerspectiveTransform(actual, should_be)
    rows, cols, ch = img.shape

    img = cv2.warpPerspective(img, pers_M, (cols, rows))

    return img[:, :1080]


def mark_ArUco_image(image, ArUco_details_dict, ArUco_corners):
    for ids, details in ArUco_details_dict.items():
        center = details[0]

        cv2.circle(image, center, 5, (0, 0, 255), -1)

        corner = ArUco_corners[int(ids)]
        cv2.circle(image, (int(corner[0][0]), int(
            corner[0][1])), 5, (50, 50, 50), -1)
        cv2.circle(image, (int(corner[1][0]), int(
            corner[1][1])), 5, (0, 255, 0), -1)
        cv2.circle(image, (int(corner[2][0]), int(
            corner[2][1])), 5, (128, 0, 255), -1)
        cv2.circle(image, (int(corner[3][0]), int(
            corner[3][1])), 5, (25, 255, 255), -1)

        tl_tr_center_x = int((corner[0][0] + corner[1][0]) / 2)
        tl_tr_center_y = int((corner[0][1] + corner[1][1]) / 2)

        cv2.line(image, center, (tl_tr_center_x,
                 tl_tr_center_y), (255, 0, 0), 5)
        display_offset = int(
            math.sqrt((tl_tr_center_x - center[0])**2 + (tl_tr_center_y - center[1])**2))
        cv2.putText(image, str(ids), (center[0] + int(display_offset/2),
                    center[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        # angle = details[1]
        # cv2.putText(image, str(angle), (center[0] - display_offset, center[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    return image
