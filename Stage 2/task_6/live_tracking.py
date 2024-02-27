'''
* Team Id :         1470
* Author List :     Parth Jain, Anikesh Kulal, Akash Kolakkal, Keshav Jha
* Filename:         live_tracking.py
* Theme:            GeoGuide (GG)
* Functions:        get_lat_lon
* Global Variables: None
'''
import csv
from utilities import calculate_distance

def get_lat_lon(center, angle):
    '''
    * Function Name:    get_lat_lon
    * Input:            center -> A tuple containing the x and y coordinates 
    *                   of the center of the ArUco marker
    *                   angle -> The angle of the ArUco marker
    * Output:           lat -> Latitude of the current position
    *                   lon -> Longitude of the current position
    * Logic:            This function takes the center and angle of the ArUco marker
    *                   and returns the latitude and longitude of the current position
    *                   of the bot using the lat_lon.csv file
    * Example Call:     lat, lon = get_lat_lon((100, 100), 90)
    '''

    # Read the lat_lon.csv file and store the data in a dictionary for easy access
    positions = {}
    with open('lat_lon.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            positions[row[0]] = [int(row[1]), int(row[2]), float(row[3]), float(row[4])]

    # reducing the angle to one of 0, 90, 180, 270, or None.
    # This is done to extract the bot's current general direction
    if int(angle) in list(range(-180, -145)) or int(angle) in list(range(145, 180)):
        angle = 0
    elif int(angle) in range(65, 125):
        angle = 90
    elif int(angle) in list(range(-45, 0)) or int(angle) in list(range(0, 45)):
        angle = 180
    elif int(angle) in range(-135, -25):
        angle = 270
    else:
        return None, None

    closest_dists = [100000, 100000]
    closest_ids = [None, None]

    # The following code is used to find the two closest ArUco markers to the bot
    # based on the bot's current direction
    if angle == 0 or angle == 180:

        # if the bot is facing in the x-direction, 
        # we extract all the control points (near aruco markers) that lie within 120 pixels in the opposite axis (Y), 
        # and then find the two closest control points.
        # These points can be used to calculate the latitude and longitude of the bot
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

        # Based on whichever direction the bot is facing, 
        # we assign the forward and backward control points
        # This can be calculated if the said control points appear before 
        # or after the bot in the same axis (X)
        if angle == 0:
            forward = closest_ids[0] if positions[closest_ids[0]][1] < positions[closest_ids[1]][1] else closest_ids[1]
            backward = closest_ids[1] if forward == closest_ids[0] else closest_ids[0]

        elif angle == 180:
            backward = closest_ids[0] if positions[closest_ids[0]][1] < positions[closest_ids[1]][1] else closest_ids[1]
            forward = closest_ids[1] if backward == closest_ids[0] else closest_ids[0]

    # Similar to the above code, we find the two closest control points
    # if the bot is facing in the y-direction
    elif angle == 90 or angle == 270:
        for key, values in positions.items():
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
        
        # Based on whichever direction the bot is facing,
        # we assign the forward and backward control points
        # This can be calculated if the said control points appear before
        # or after the bot in the same axis (Y)
        if angle == 90:
            backward = closest_ids[0] if positions[closest_ids[0]][0] < positions[closest_ids[1]][0] else closest_ids[1]
            forward = closest_ids[1] if backward == closest_ids[0] else closest_ids[0]

        elif angle == 270:
            forward = closest_ids[0] if positions[closest_ids[0]][0] < positions[closest_ids[1]][0] else closest_ids[1]
            backward = closest_ids[1] if forward == closest_ids[0] else closest_ids[0]

    else:
        # print("Aruco Not detected")
        pass

    # calculate the ratio of the distance of the bot from the forward control point 
    # w.r.t the distance between the forward and backward control points
    m = calculate_distance(center, positions[forward][0:2]) / calculate_distance(
        positions[forward][0:2], positions[backward][0:2])
    n = 1 - m

    # Using the obtained ratio to calculate the latitude and longitude of the 
    # bot using the values obtained from the csv
    lat = m * positions[backward][2] + n * positions[forward][2]
    lon = m * positions[backward][3] + n * positions[forward][3]

    return lat, lon
