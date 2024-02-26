import cv2
import csv
from utilities import detect_ArUco_details, calculate_distance


def get_lat_lon(center, angle):

    positions = {}
    with open('lat_lon.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            positions[row[0]] = [int(row[1]), int(
                row[2]), float(row[3]), float(row[4])]

    if int(angle) in list(range(-180, -145)) or int(angle) in list(range(145, 180)):
        angle = 0
    elif int(angle) in range(60, 120):
        angle = 90
    elif int(angle) in list(range(-35, 0)) or int(angle) in list(range(0, 35)):
        angle = 180
    elif int(angle) in range(-120, -35):
        angle = 270
    else:
        return None, None

    closest_dists = [100000, 100000]
    closest_ids = [None, None]

    if angle == 0 or angle == 180:
        for key, values in positions.items():

            distance = calculate_distance(center, values[0:2])
            if abs(center[0] - values[0]) < 120:
                if distance < closest_dists[0]:
                    closest_dists[1] = closest_dists[0]
                    closest_ids[1] = closest_ids[0]
                    closest_dists[0] = distance
                    closest_ids[0] = key
                elif distance < closest_dists[1]:
                    closest_dists[1] = distance
                    closest_ids[1] = key

        if angle == 0:
            forward = closest_ids[0] if positions[closest_ids[0]
                                                  ][1] < positions[closest_ids[1]][1] else closest_ids[1]
            backward = closest_ids[1] if forward == closest_ids[0] else closest_ids[0]

        elif angle == 180:
            backward = closest_ids[0] if positions[closest_ids[0]
                                                   ][1] < positions[closest_ids[1]][1] else closest_ids[1]
            forward = closest_ids[1] if backward == closest_ids[0] else closest_ids[0]

    elif angle == 90 or angle == 270:
        for key, values in positions.items():
            # if (100 < values[1] < 300) or (480 < values[1] < 610) or (860 < values[1]):
            if abs(center[1] - values[1]) < 120:
                distance = calculate_distance(center, values[0:2])
                if distance < closest_dists[0]:
                    closest_dists[1] = closest_dists[0]
                    closest_ids[1] = closest_ids[0]
                    closest_dists[0] = distance
                    closest_ids[0] = key
                elif distance < closest_dists[1]:
                    closest_dists[1] = distance
                    closest_ids[1] = key

        if angle == 90:
            backward = closest_ids[0] if positions[closest_ids[0]
                                                   ][0] < positions[closest_ids[1]][0] else closest_ids[1]
            forward = closest_ids[1] if backward == closest_ids[0] else closest_ids[0]

        elif angle == 270:
            forward = closest_ids[0] if positions[closest_ids[0]
                                                  ][0] < positions[closest_ids[1]][0] else closest_ids[1]
            backward = closest_ids[1] if forward == closest_ids[0] else closest_ids[0]

    else:
        # print("Aruco Not detected")
        pass

    m = calculate_distance(center, positions[forward][0:2]) / calculate_distance(
        positions[forward][0:2], positions[backward][0:2])
    n = 1 - m

    lat = m * positions[backward][2] + n * positions[forward][2]
    lon = m * positions[backward][3] + n * positions[forward][3]

    return lat, lon


if __name__ == "__main__":

    image_path = 'sample5.jpg'
    file_path = 'output.csv'

    img = cv2.imread(image_path)
    aruco_dict, corners = detect_ArUco_details(img)

    center = aruco_dict[100][0]
    angle = aruco_dict[100][1]

    lat, lon = get_lat_lon(center, angle)

    with open(file_path, 'w', newline='') as csv_file:

        csv_writer = csv.writer(csv_file)

        data = [
            ['lat', 'lon'],
            [lat, lon]
        ]

        csv_writer.writerows(data)
