'''
* Team Id :         1470
* Author List :     Parth Jain, Anikesh Kulal, Akash Kolakkal, Keshav Jha
* Filename:         pathfinder.py
* Theme:            GeoGuide (GG)
* Functions:        get_weights, convert_directions, get_neighbor, dijkstra, calculate_path, get_minimum_cost_path, calculate_path_string
* Global Variables: None
'''

import numpy as np
import heapq
from itertools import permutations

def get_weights():
    '''
    * Function Name:    get_weights
    * Input:            None
    * Output:           adjacency_list -> A 3d numpy array of shape (5, 5, 4) containing the weights of the edges for each node
    * Logic:            This function returns the weights of the edges 
    *                   for each node in the arena to be used in the dijkstra algorithm.
    * Example Call:     weights = get_weights()
    '''
    adjacency_list = np.empty((5, 5), dtype=object)

    # Iterating over all the nodes on the arena, both the 
    # actual nodes that are marked by black spots, and 'virtual' nodes that are present right above the events.
    for i in range(5):
        for j in range(5):
            adjacency_list[i][j] = [1, 1, 1, 1]

            # setting the weights of the edges of the nodes that are on the edges of the map to 999
            if i == 0:
                adjacency_list[i][j][0] = 999
            if i == 4:
                adjacency_list[i][j][2] = 999
            
            if j == 0:
                adjacency_list[i][j][3] = 999
            if j == 4:
                adjacency_list[i][j][1] = 999
            
            # assigning the edges that are blocked off on the arena as 999, 
            # and those who have longer distances to 1.5
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
    
    # mannually assigning some edges that are blocked off on the arena
    adjacency_list[0][2][2] = 999
    adjacency_list[1][2][0] = 999
    adjacency_list[4][4][3] = 999
    adjacency_list[4][3][1] = 999
    adjacency_list[4][4][0] = 999
    adjacency_list[3][4][2] = 999

    return adjacency_list

def convert_directions(direction_dict, current_direction):
    '''
    * Function Name:    convert_directions
    * Input:            direction_dict -> list of instructions w.r.t. the arena
    *                   current_direction -> current direction that the bot is facing
    * Output:           relative_instructions, current_direction
    * Logic:            This function takes in the direction_dict, which is a list of instructions with resprct to the arena 
    *                   and the current direction that the bot is facing,
    *                   and returns the relative instructions with respect to the bot's perspective and the updated current direction of the bot.
    * Example Call:     relative_instructions, current_direction = convert_directions(direction_dict, current_direction)
    '''

    def not_a_node(node):
        '''
        * Function Name:    not_a_node
        * Input:            node -> tuple of the node's position
        * Output:           boolean
        * Logic:            This function takes in a node and returns True if the node is an actual node on the 
        *                   arena marked by the black spots node, else False.
        * Example Call:     not_a_node((1, 2))
        '''
        return (node[0] == 0 or node[1] == 1 or node[1] == 3 or node == (4,4))

    # dictionary to convert the relative directions to the bot's perspective
    # for example, if the bot is facing 'U' and the instruction is 'U', then the bot will move 'F' in the arena
    relative_directions = {
        'U': {'U': 'F', 'R': 'R', 'D': 'B', 'L': 'L'},
        'R': {'U': 'L', 'R': 'F', 'D': 'R', 'L': 'B'},
        'D': {'U': 'B', 'R': 'L', 'D': 'F', 'L': 'R'},
        'L': {'U': 'R', 'R': 'B', 'D': 'L', 'L': 'F'},
    }

    path = list(direction_dict.keys())
    directions = list(direction_dict.values())

    all_directions = []
    relative_instructions = ""

    # converting the directions to the bot's perspective for every node, including the virtual nodes
    for i in range(len(path)):
        all_directions.append(relative_directions[current_direction][directions[i]])
        current_direction = directions[i]
    
    # Checking if the node is an actual node on the arena, and if it is, 
    # then adding the relative direction to the relative_instructions for every node in the path.
    # for clarification about virtual nodes, refer to the nodes_example.png file in the same directory
    for i in range(len(path)):
        if not_a_node(path[i]) and i != 0:
            continue
        else:
            relative_instructions += all_directions[i]
    

    return relative_instructions, current_direction

def get_neighbor(node, direction):
    '''
    * Function Name:    get_neighbor
    * Input:            node -> tuple of the node's position
    *                   direction -> direction in which the bot is moving
    * Output:           neighbor -> tuple of the neighbor's position
    * Logic:            This function takes in the node and the direction in which the bot is moving,
    *                   and returns the position of the neighbor node in the given direction.
    * Example Call:     get_neighbor((1, 2), 0)
    '''
    i, j = node
    if direction == 0 and i > 0:  # direction 0 is Up
        return (i - 1, j)
    elif direction == 1 and j < 4:  # 1 is Right
        return (i, j + 1)
    elif direction == 2 and i < 4:  # 2 is Down
        return (i + 1, j)
    elif direction == 3 and j > 0:  # 3 is Left
        return (i, j - 1)
    return None

def dijkstra(start_index, end_index):
    '''
    * Function Name:    dijkstra
    * Input:            start_index -> index of the start node
    *                   end_index -> index of the end node
    * Output:           direction_dict -> dictionary containing the node's coordinates and directions 
    *                   to reach the next node in order to traverse the whole path
    *                   cost -> cost to reach the end node from the start node
    * Logic:            This function takes in the start and end index of the nodes on the arena,
    *                   and returns the direction_dict, which is a dictionary containing the node's coordinates and 
    *                   directions to reach the end node
    *                   and the cost to reach the end node from the start node.
    * Example Call:     dijkstra('S', 'A')
    '''

    # dictionary containing the positions of the events on the arena
    # S is the start and end point
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

    # getting the weights of the edges of the nodes on the arena
    weights = get_weights()

    # initializing the distances as infinite and previous_nodes dictionaries
    distances = {(i, j): np.inf for i in range(5) for j in range(5)}
    previous_nodes = {(i, j): None for i in range(5) for j in range(5)}

    distances[start] = 0

    queue = [(0, start)]

    # dijkstra algorithm
    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # iterating over all the neighbors of the current node and updating the distances and previous_nodes
        # if the distance to the neighbor is less than the current distance, then updating the distances and previous_nodes
        for direction, weight in enumerate(weights[current_node[0]][current_node[1]]):
            neighbor = get_neighbor(current_node, direction)
            if neighbor is not None:
                tentative_distance = distances[current_node] + weight
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(queue, (tentative_distance, neighbor))

    # getting the path from the start node to the end node
    path = []
    while end is not None:
        path.append(end)
        end = previous_nodes[end]
    
    # reversing the path to get the correct order of the nodes from the start to the end node
    path.reverse()

    difference = (path[-1][0] - path[-2][0], path[-1][1] - path[-2][1])
    path.append((path[-1][0] + difference[0], path[-1][1] + difference[1]))
    # print(path)

    # calculating the cost to reach the end node from the start node
    cost = distances[node_dict[end_index]]

    # converting the path to the directions to reach the end node by using the difference between the current and previous nodes
    direction_dict = {}
    for i in range(1, len(path)):

        # checking the difference between the current and previous nodes to get the direction to reach the currrent node
        diff = (path[i][0] - path[i-1][0], path[i][1] - path[i-1][1])

        if diff == (0, 1):
            direction_dict[path[i-1]] = 'R'
        elif diff == (-1, 0):
            direction_dict[path[i-1]] = 'U'
        elif diff == (1, 0):
            direction_dict[path[i-1]] = 'D'
        elif diff == (0, -1):
            direction_dict[path[i-1]] = 'L'

    return direction_dict, cost

def calculate_path(path):
    '''
    * Function Name:    calculate_path
    * Input:            path -> list of events to be visited in order.
    * Output:           relative_path_complete -> instructions to traversed by the bot to 
    *                   complete the whole path w.r.t. the bot's perspective.
    *                   cost -> cost to traverse the path
    * Logic:            This function takes in the path, which is a list of events 
    *                   to be visited in order,
    *                   and returns the relative_path_complete, which is the 
    *                   complete relative path to traverse the path,
    *                   and the cost to traverse the whole path.
    * Example Call:     relative_path_complete, cost = calculate_path(['S', 'A', 'B', 'S'])
    '''

    # initializing the current direction as 'U' and the relative_path_complete as an empty string
    current_direction = "U"
    relative_path_complete = ""
    cost = 0
    
    # iterating over all the events to be visited one by one, 
    # and calculating the relative directions to reach the next event
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i+1]

        directions, temp_cost = dijkstra(start, end)
        cost += temp_cost

        relative_directions, current_direction = convert_directions(directions, current_direction)

        relative_path_complete += relative_directions
    
    relative_path_complete = relative_path_complete[:-1] + 'E'
    try:
        # for the edge case where the last event is 'A', then adding 'L' to the 
        # relative_path_complete indicating the need to take a left turn before completing the run
        if path[-2] == 'A':
            relative_path_complete += 'L'
    except(IndexError):
        pass
    
    # adding an 'F' as the bot's first step to start the run
    relative_path_complete = 'F' + relative_path_complete
    
    # print("Path : " + str(path) + "\nCost : " + str(cost) + "\nRelative Path : " + relative_path_complete)

    return relative_path_complete, cost

def get_minimum_cost_path(paths: list):
    '''
    * Function Name:    get_minimum_cost_path
    * Input:            paths -> list of paths to be compared
    * Output:           relative_path -> instructions to traversed by the bot to
    *                   complete the whole path w.r.t. the bot's perspective.
    *                   path -> path with the minimum cost
    * Logic:            This function takes in the paths, which is a list of paths to be compared,
    *                   and returns the relative_path, which is the complete relative path to 
    *                   traverse the path,
    *                   and the path with the minimum cost.
    * Example Call:     relative_path, path = get_minimum_cost_path(paths)
    '''
    minimum_cost = 100

    # iterating over all the paths and calculating the cost to traverse the path
    # and finding the path with the minimum cost to return
    for i in paths:
        return_path, cost = calculate_path(i)
        if cost < minimum_cost:
            minimum_cost = cost
            path = i
            relative_path = return_path
    
    return relative_path, path

def calculate_path_string(labels_dict: dict):
    '''
    * Function Name:    calculate_path_string
    * Input:            labels_dict -> dictionary containing the events and their locations
    * Output:           relative_path -> instructions to traversed by the bot to
    *                   complete the whole path w.r.t. the bot's perspective.
    *                   path[1:-1] -> path with the minimum cost
    * Logic:            This function takes in the labels_dict, which is a dictionary containing the 
    *                   detected events and their locations,
    *                   and returns the relative_path, which is the complete 
    *                   relative path to traverse the path and visit al the events 
    *                   according to their priorities,
    *                   and the path with the minimum cost.
    * Example Call:     relative_path, path = calculate_path_string(labels_dict)
    '''

    # dictionary containing the count of the events detected and in order of their priorities
    event_count = {
        'Fire': 0, 
        'Destroyed buildings': 0, 
        'Humanitarian Aid and rehabilitation': 0, 
        'Military Vehicles': 0, 
        'Combat': 0,
        }
    
    path = ["S"]
    duplicates = []

    # iterating over all the events detected and updating the event_count dictionary
    for event in event_count.keys():
        temp = []
        for location, present_event in labels_dict.items():
            if event == present_event:
                event_count[event] += 1
                path.append(location)
                temp.append(len(path) - 1)

        # checking if there are multiple events of the same type, 
        # and adding the indexes of the events to the duplicates list
        if len(temp) > 1:
            duplicates.append(temp)
    
    path.append("S")
    paths = []
    paths.append(path)

    # if any duplicates are present, then calculating the permutations of the paths
    # and adding the paths to the paths list, which will be used to calculate 
    # the path with the minimum cost
    for duplicate in duplicates:
        for p in permutations(path[duplicate[0]: duplicate[-1] + 1]):
            for i in paths:
                temp_path = i[:duplicate[0]]
                temp_path.extend(p)
                temp_path.extend(i[duplicate[-1] + 1:])
                if temp_path not in paths:
                    paths.append(temp_path)

    # getting the path with the minimum cost
    relative_path, path = get_minimum_cost_path(paths)

    # print(relative_path, path[1:-1])
    return relative_path, path[1:-1]


if __name__ == "__main__":
    # for test purpose
    path = ['S', 'A', 'S']
    relative_path = calculate_path(path)