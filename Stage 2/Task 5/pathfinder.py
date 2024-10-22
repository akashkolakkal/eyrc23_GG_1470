'''
# Team ID:          1470
# Theme:            Geo Guide
# Author List:      Parth Jain, Akash Kolakkal, Anikesh Kulal, Keshav Jha
# Filename:         pathfinder.py
# Functions:        get_weights, convert_directions, get_neighbor, dijkstra, calculate_path
# Global variables: conn, stop_server, s
'''


'''
0 0 0 0 0 
0 0 0 0 0
0 2 0 0 0
0 0 0 0 0
1 0 0 0 0

start = (0, 5)
end = (2, 1)

[F, R, F]
'''

import numpy as np
import heapq

def get_weights():
    adjacency_list = np.empty((5, 5), dtype=object)

    # 0 = up, 1 = right, 2 = down, 3 = left

    for i in range(5):
        for j in range(5):
            adjacency_list[i][j] = [1, 1, 1, 1]
            if i == 0:
                adjacency_list[i][j][0] = 999
            if i == 4:
                adjacency_list[i][j][2] = 999
            
            if j == 0:
                adjacency_list[i][j][3] = 999
            if j == 4:
                adjacency_list[i][j][1] = 999
            
            if j == 1:
                adjacency_list[i][j][0] = 999
                adjacency_list[i][j][2] = 999
                adjacency_list[i][j][1] = 1.5
            if j == 3:
                adjacency_list[i][j][0] = 999
                adjacency_list[i][j][2] = 999
                adjacency_list[i][j][3] = 1.5
            if j == 2:
                adjacency_list[i][j][1] = 1.5
                adjacency_list[i][j][3] = 1.5
    
    adjacency_list[0][2][2] = 999
    adjacency_list[1][2][0] = 999
    adjacency_list[0][2][1] = 1.75
    adjacency_list[1][2][3] = 1.75

    return adjacency_list

def convert_directions(direction_dict, facing):
    def not_a_node(node):
        return (node[0] == 0 or node[1] == 1 or node[1] == 3 or node == (4,4))

    relative_directions = {
        'U': {'U': 'F', 'R': 'R', 'D': 'B', 'L': 'L'},
        'R': {'U': 'L', 'R': 'F', 'D': 'R', 'L': 'B'},
        'D': {'U': 'B', 'R': 'L', 'D': 'F', 'L': 'R'},
        'L': {'U': 'R', 'R': 'B', 'D': 'L', 'L': 'F'},
    }
    current_direction = facing

    path = list(direction_dict.keys())
    directions = list(direction_dict.values())
    all_directions = []
    relative_instructions = ""

    for i in range(len(path)):
        all_directions.append(relative_directions[current_direction][directions[i]])
        current_direction = directions[i]
    
    for i in range(len(path)):
        if not_a_node(path[i])   and i != 0:
            continue
        else:
            relative_instructions += all_directions[i]
    

    return relative_instructions, current_direction

def get_neighbor(node, direction):
    i, j = node
    if direction == 0 and i > 0:  # Up
        return (i - 1, j)
    elif direction == 1 and j < 4:  # Right
        return (i, j + 1)
    elif direction == 2 and i < 4:  # Down
        return (i + 1, j)
    elif direction == 3 and j > 0:  # Left
        return (i, j - 1)
    return None

def dijkstra(start_index, end_index):


    node_dict = {
        "A": (4,1),
        "B": (3,3),
        "C": (2,3),
        "D": (2,1),
        "E": (0,1),
        "S": (4,0)
    }

    start = node_dict[start_index]
    end = node_dict[end_index]
    weights = get_weights()


    distances = {(i, j): np.inf for i in range(5) for j in range(5)}
    previous_nodes = {(i, j): None for i in range(5) for j in range(5)}
    distances[start] = 0

    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        for direction, weight in enumerate(weights[current_node[0]][current_node[1]]):
            neighbor = get_neighbor(current_node, direction)
            if neighbor is not None:
                tentative_distance = distances[current_node] + weight
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(queue, (tentative_distance, neighbor))

    path = []
    while end is not None:
        path.append(end)
        end = previous_nodes[end]
    path.reverse()

    difference = (path[-1][0] - path[-2][0], path[-1][1] - path[-2][1])
    path.append((path[-1][0] + difference[0], path[-1][1] + difference[1]))
    # print(path)

    direction_dict = {}

    for i in range(1, len(path)):
        diff = (path[i][0] - path[i-1][0], path[i][1] - path[i-1][1])
        if diff == (0, 1):
            direction_dict[path[i-1]] = 'R'
        elif diff == (-1, 0):
            direction_dict[path[i-1]] = 'U'
        elif diff == (1, 0):
            direction_dict[path[i-1]] = 'D'
        elif diff == (0, -1):
            direction_dict[path[i-1]] = 'L'

    return direction_dict

def calculate_path(path):
    current_direction = "U"
    relative_path_complete = ""
    
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i+1]
        print(start, end)
        directions = dijkstra(start, end)
        relative_directions, current_direction = convert_directions(directions, current_direction)

        relative_path_complete += relative_directions
    
    relative_path_complete = relative_path_complete[:-1] + 'E'
    if path[-2] == 'A':
        relative_path_complete += 'L'
    
    if path[1] == 'A':
        relative_path_complete = 'R' + relative_path_complete[1:]
    else:
        relative_path_complete = 'S' + relative_path_complete[1:]
    
    relative_path_complete = 'F' + relative_path_complete
    
    print("Path : " + str(path))

    print(relative_path_complete)
    return relative_path_complete


    
if __name__ == "__main__":

    path = ['S', 'A', 'D', 'C', 'B', 'S']
    relative_path = calculate_path(path)
