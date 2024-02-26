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
from itertools import permutations

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
    adjacency_list[4][4][3] = 999
    adjacency_list[4][3][1] = 999
    adjacency_list[4][4][0] = 999
    adjacency_list[3][4][2] = 999

    return adjacency_list

def convert_directions2(direction_dict, facing):

    def not_a_node(node):
        return (node[0] == 0 or node[1] == 1 or node[1] == 3 or node == (4,4))

    relative_directions = {
        'U': {'U': 'F', 'R': 'R', 'D': 'B', 'L': 'L'},
        'R': {'U': 'L', 'R': 'F', 'D': 'R', 'L': 'B'},
        'D': {'U': 'B', 'R': 'L', 'D': 'F', 'L': 'R'},
        'L': {'U': 'R', 'R': 'B', 'D': 'L', 'L': 'F'},
    }

    relative_path = []
    current_direction = facing

    path = list(direction_dict.keys())
    directions = list(direction_dict.values())
    new_path = []

    for i in range(len(path)):
        if (not_a_node(path[i]) or path[i] in [(0,0), (0,4), (4,4)]) and i != 0:
            if directions[i] != directions[i-1]:
                continue
            else:
                new_path.append(path[i])
        else:
            new_path.append(path[i])
    
    # print(new_path)
    

    last_node = (10,10)

    for current_node, direction in direction_dict.items():
        
        if current_node in new_path:
            relative_path.append(relative_directions[current_direction][direction])
            current_direction = direction
        
        if current_node == (0,0) and last_node == (0,1):
            current_direction = 'D'
        elif current_node == (0,0) and last_node == (1,0):
            current_direction = 'R'
        
        elif current_node == (0,4) and last_node == (0,3):
            current_direction = 'D'
        elif current_node == (0,4) and last_node == (1,4):
            current_direction = 'L'
        
        elif current_node == (4,4) and last_node == (4,3):
            current_direction = 'U'
        elif current_node == (4,4) and last_node == (3,4):
            current_direction = 'L'
        
        if current_node in [(0,0), (0,4), (4,4)]:
            relative_path.pop(-1)
        
        last_node = current_node


    return relative_path, current_direction

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

    return direction_dict, distances[node_dict[end_index]]

def calculate_path(path):
    current_direction = "U"
    relative_path_complete = ""
    cost = 0
    
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i+1]
        # print(start, end)
        directions, temp_cost = dijkstra(start, end)
        cost += temp_cost

        relative_directions, current_direction = convert_directions(directions, current_direction)

        relative_path_complete += relative_directions
    
    relative_path_complete = relative_path_complete[:-1] + 'E'
    try:
        if path[-2] == 'A':
            relative_path_complete += 'L'
    except(IndexError):
        pass
    # if path[1] == 'A':
    #     relative_path_complete = 'R' + relative_path_complete[1:]
    # else:
    #     relative_path_complete = 'F' + relative_path_complete[1:]
    
    relative_path_complete = 'F' + relative_path_complete
    
    # print("Path : " + str(path) + "\nCost : " + str(cost) + "\nRelative Path : " + relative_path_complete)

    return relative_path_complete, cost

def get_minimum_cost_path(paths: list):
    minimum_cost = 100
    for i in paths:
        return_path, cost = calculate_path(i)
        if cost < minimum_cost:
            minimum_cost = cost
            path = i
            complete_path = return_path
    
    return complete_path, path

def calculate_path_string(labels_dict: dict):
    event_count = {
        'Fire': 0, 
        'Destroyed buildings': 0, 
        'Humanitarian Aid and rehabilitation': 0, 
        'Military Vehicles': 0, 
        'Combat': 0,
        }
    
    path = ["S"]
    duplicates = []

    for event in event_count.keys():
        temp = []
        for location, present_event in labels_dict.items():
            if event == present_event:
                event_count[event] += 1
                path.append(location)
                temp.append(len(path) - 1)

        if len(temp) > 1:
            duplicates.append(temp)
    
    path.append("S")
    paths = []
    paths.append(path)


    for duplicate in duplicates:
        for p in permutations(path[duplicate[0]: duplicate[-1] + 1]):
            for i in paths:
                temp_path = i[:duplicate[0]]
                temp_path.extend(p)
                temp_path.extend(i[duplicate[-1] + 1:])
                if temp_path not in paths:
                    paths.append(temp_path)

    complete_path, path = get_minimum_cost_path(paths)

    # print(complete_path, path[1:-1])
    return complete_path, path[1:-1]

    
if __name__ == "__main__":

    path = ['S', 'A', 'S']
    relative_path = calculate_path(path)
