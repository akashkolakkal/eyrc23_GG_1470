import numpy as np
import cv2
from cv2 import aruco
import math
import matplotlib.pyplot as plt
import csv
from task_4a import return_labels_dict
from pathfinder import calculate_path
from sympy import symbols, Eq, solve, sqrt


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
            dist = math.sqrt((details[0][0] - center[0])
                             * 2 + (details[0][1] - center[1])*2)
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


def calculate_distance(x1, y1, x2, y2):
    return sqrt((x1 - x2)*2 + (y1 - y2)*2)


def get_closest_ids(ArUco_details_dict):
    closest_dist = []
    closest_dist1 = 10000000
    closest_dist2 = 10000000
    closest_dist3 = 10000000
    closest_id1 = 42
    closest_id2 = 42
    closest_id3 = 42

    try:
        center = ArUco_details_dict[100][0]

        csv_file = open('lat_long.csv', 'r')

        csv_reader = csv.reader(csv_file)

        for id, details in ArUco_details_dict.items():
            dist = math.sqrt((details[0][0] - center[0])
                             * 2 + (details[0][1] - center[1])*2)
            if dist < closest_dist1 and id != 100:
                closest_dist1 = dist
                closest_id1 = id
            if dist < closest_dist2 and id != 100 and id != closest_id1:
                closest_dist2 = dist
                closest_id2 = id
            if dist < closest_dist3 and id != 100 and id != closest_id1 and id != closest_id2:
                closest_dist3 = dist
                closest_id3 = id

        for row in csv_reader:
            try:
                if int(row[0]) == int(closest_id1):
                    closest_dist.append([row[1], row[2]])
                if int(row[0]) == int(closest_id2):
                    closest_dist.append([row[1], row[2]])
                if int(row[0]) == int(closest_id3):
                    closest_dist.append([row[1], row[2]])
            except:
                pass
        csv_file.close()
        return closest_dist

    except:
        print("ArUco marker 1 not detected.")
    return None, None


def getexactposition(aruco1x, aruco1y, aruco2x, aruco2y, aruco3x, aruco3y, aruco1d, aruco2d):
    x, y = symbols('x y')

    x1, y1 = aruco1x, aruco1y
    x2, y2 = aruco2x, aruco2y

    equation1 = Eq(sqrt((x1 - x)*2 + (y1 - y)*2), aruco1d)
    equation2 = Eq(sqrt((x2 - x)*2 + (y2 - y)*2), aruco2d)

    solution = solve((equation1, equation2), (x, y))

    if len(solution) == 2:
        root1, root2 = solution[0], solution[1]

        distance_root1 = calculate_distance(
            root1[0], root1[1], aruco3x, aruco3y)
        distance_root2 = calculate_distance(
            root2[0], root2[1], aruco3x, aruco3y)

        if distance_root1 < distance_root2:
            return root1
        else:
            return root2
    elif len(solution) == 1:
        return solution[0]
    else:
        return None


def did_reach(center, event):
    events = {
        "A": (),
        "B": (),
        "C": (),
        "D": (),
        "E": ()
    }

    if math.sqrt((center[0] - events[event][0])*2 + (center[1] - events[event][1])*2) <= 50:
        return True
    return False


def get_arena(img):
    actual = np.float32([[396, 6], [1385, 77], [1392, 1065], [313, 1063]])
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
            math.sqrt((tl_tr_center_x - center[0])*2 + (tl_tr_center_y - center[1])*2))
        cv2.putText(image, str(ids), (center[0] + int(display_offset/2),
                    center[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        # angle = details[1]
        # cv2.putText(image, str(angle), (center[0] - display_offset, center[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    return image


if __name__ == '__main__':

    # ['destroed', 'fire', 'None', 'military', 'combat']
    # labels_dict = return_labels_dict()
    # priority_list = ['fire', 'destroyed_buildings', 'human_aid_rehabilitation', 'military_vehicles', 'combat']
    # event_priority = []
    # path = ["S"]

    # for label in labels_dict.values():
    #     if label != 'None':
    #         priority = priority_list.index(label)
    #         event_priority.append(priority)

    # # [1, 0, 2, 3, 4]

    # while(len(event_priority) > 0):
    #     min_index = event_priority.index(min(event_priority))
    #     event_priority.pop(min_index)
    #     path.append(chr(min_index + 65))

    # path.append("S")

    # complete_path = calculate_path(path)

    # TODO Send to bot

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    file_path = 'task_4b.csv'

    # for live camera feed

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
        # frame = mark_ArUco_image(frame, ArUco_details_dict, ArUco_corners)
        try:
            bot_aruco_center = ArUco_details_dict[100][0]
            lat, lon = None, None

            if (i % 10 == 0):
                closest_aruco_details = get_closest_ids(ArUco_details_dict)

                arucod1 = calculate_distance(
                    closest_aruco_details[0][0], closest_aruco_details[0][1], bot_aruco_center[0], bot_aruco_center[1])
                arucod2 = calculate_distance(
                    closest_aruco_details[1][0], closest_aruco_details[1][1], bot_aruco_center[0], bot_aruco_center[1])

                lat, lon = getexactposition(closest_aruco_details[0][0], closest_aruco_details[0][1], closest_aruco_details[1]
                                            [0], closest_aruco_details[1][1], closest_aruco_details[2][0], closest_aruco_details[2][1], arucod1, arucod2)

            # path.pop(-1)
            # path.pop(0)
            # event = path[0]
            # if did_reach(ArUco_details_dict[1][0], event):
            #     path.pop(0)

            if lat != None and lon != None:
                with open(file_path, 'w', newline='') as csv_file:

                    csv_writer = csv.writer(csv_file)

                    data = [
                        ['lat', 'lon'],
                        [lat, lon]
                    ]

                    csv_writer.writerows(data)
        except:
            pass

        # frame = mark_ArUco_image(frame, ArUco_details_dict, ArUco_corners)
        
        frame = cv2.resize(frame, (950, 950))
        cv2.imshow("ArUco Marker Detection", frame)
        i += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
