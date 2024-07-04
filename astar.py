'''
Ludwig Krause: 209200612 
Willem Schlüter: 220201009 
Sadegh Hajimirzamohammadi: 221202356
Lukas Stahl: 221202203
'''

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


def a_star_search(goal, board, mode):
    '''
    Berechnet den kürzesten Pfad zwischen zwei Koordinaten auf dem Spielfeld, umgeht dabei Hindernisse, berechnet mit dem A*-Algorithmus.

    Parameter:
    ----------
    goal: (x,y)-Tupel für Koordinaten auf dem Feld
    board: Board Objekt
    mode: String "hunt", "food"

    Return:
    ----------
    next_move: String "up", "down", "left", "right"
    '''

    start = board.head
    start = (start['x'], start['y'])

    frontier = []
    heapq.heappush(frontier, (0, start))
    field_before = {}
    cost_till_now = {}
    field_before[start] = None
    cost_till_now[start] = 0

    while not len(frontier) == 0:
        current_field = heapq.heappop(frontier)[1]

        if current_field == goal:
            break

        for next_possible_field in get_possible_fields(current_field, board, mode):
            new_cost = cost_till_now[current_field] + 1
            if next_possible_field not in cost_till_now or new_cost < cost_till_now[next_possible_field]:
                cost_till_now[next_possible_field] = new_cost
                prior = new_cost + heuristic(goal, next_possible_field)
                heapq.heappush(frontier, (prior, next_possible_field))
                field_before[next_possible_field] = current_field

    # Reconstruct path
    if goal not in field_before:
        return "no_move"

    current_field = goal
    path = []
    while current_field != start:
        path.append(current_field)
        current_field = field_before[current_field]
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


def get_possible_fields(node, board, mode):
    '''
    Hilfsfunktion für a_star_search, die alle möglichen nächsten Felder für einen bestimmten Knoten auf deren Inhalte prüft. Im 'food' Modus, sind nur Felder mit Nahrung oder leeren Felder möglich. Im 'hunt' Modus sind Nahrung, leerer Felder und Köpfe anderer Schlanges möglich.

    Parameter:
    ----------
    node: (x,y)-Tupel für Koordinaten auf dem Feld
    board: Board Objekt
    mode: String "hunt", "food"

    Return:
    ----------
    possible_fields: [(x1,y1),...,(x4,y4)] Liste von (x,y)-Tupels Koordinaten auf dem Feld
    '''
    nodeX = int(node[0])
    nodeY = int(node[1])

    possible_fields = []

    directions_values = board.directions_values_for_node(nodeX, nodeY)
    directions_coordinates = board.directions_coordinates_for_node(
        nodeX, nodeY)

    if mode == 'food':
        for k, v in directions_values.items():
            if v == 'f_' or v == '__':
                possible_field = directions_coordinates[k]
                possible_fields.append(possible_field)

    elif mode == 'hunt':
        for k, v in directions_values.items():
            if 'h' in v or v == 'f_' or v == '__':
                possible_field = directions_coordinates[k]
                possible_fields.append(possible_field)
    return possible_fields
