import heapq
import numpy as np


def heuristic(a, b):
    '''
    Erstellt die Distanz zwischen zwei Koordinaten, die als Heuristik im A*-Algorithmus verwendet wird.

    Parameter:
    ----------
    a, b: (x,y)-Tupel für Koordinaten auf dem Feld.

    Return:
    ----------
    int
    '''
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(goal, game_state, board):

    start = board.head
    start = (start['x'], start['y'])

    def get_possible_fields(node):
        nodeX = int(node[0])
        nodeY = int(node[1])

        possible_fields = []

        directions_values = board.directions_values_for_node(nodeX, nodeY)
        directions_coordinates = board.directions_coordinates_for_node(
            nodeX, nodeY)

        for k, v in directions_values.items():
            if v == 'f_' or v == '__':
                possible_field = directions_coordinates[k]
                possible_fields.append(possible_field)
        return possible_fields

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not len(frontier) == 0:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next in get_possible_fields(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    # Reconstruct path
    if goal not in came_from:
        return "no_move"

    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    if len(path) < 2:
        next_move = "no_move"
    else:
        next_step = path[1]

        if next_step[0] < board.head["x"]:
            next_move = "left"
        elif next_step[0] > board.head["x"]:
            next_move = "right"
        elif next_step[1] < board.head["y"]:
            next_move = "down"
        elif next_step[1] > board.head["y"]:
            next_move = "up"

    print(np.rot90(board.board))
    directions_values = board.directions_values_for_node(
        board.head['x'], board.head['y'])
    print(f'head_directions: \n {directions_values}')
    print(f'path: \n {path}')

    return next_move
