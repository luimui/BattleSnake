# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
from board import Board
from astar import a_star_search, heuristic
from possible_safe_moves import simple_safe_moves, head_collision_safe_moves
''''''


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "MySnake",  # TODO: Your Battlesnake Username
        "color": "#FF0000",  # TODO: Choose color
        "head": "caffeine",  # TODO: Choose head
        "tail": "coffee",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:
    '''
    Diese Methode ist die Hauptmethode, die aufgerufen wird, um einen Move Request vom BattleSnake-Server mit einer Bewegungsrichtung für den nächsten Zug zurückzugeben.

    Hierarchisch werden einzelne Situationen abgeprüft und nicht sichere Züge markiert. Kern ist dabei der A*-Alogrithmus zur Bestimmung des Pfads zum dichtesten Ziel.
    Existiert kein Futter:                                      Zufälliger sicherer Zug
    Exisitiert Futter:                                          A* zum nächsten Futter
        Head-Kollision möglich und Gegner kleiner:              A* zum nächsten Futter  
    Findet A* keinen Pfad oder Head-Kollision nicht sicher:     Zufälliger sicherer Zug
    Wird gar kein sicher Zug gefunden:                          {"move": "up"}  

    Ziele können dabei Futter oder die Köpfe der anderen Schlangen sein, wenn alle anderen Schlangen wenigstens 2 Stück kleiner sind als unsere Schlange.
    
    Dafür wird beim Aufruf ein Board-Objekt erstellt, das die aktuelle Spiel-Informationen enthält.

    Parameter:
    ----------
    game_state: dict, komplexes Objekt welches das Board, die Snakes, Futter, usw. repräsentiert.

    Return:
    ----------
    next_move: dict {"move": "right"}
    '''

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    board = Board(game_state)

    # If there is food, use A star algorihm
    # If A star found no possible path, use simple_safe_moves
    food = game_state['board']['food']
    my_head = game_state['you']['head']

    if (board.max_length_others + 2 <= board.length) and board.health > 20:
        print(f'HUNTING MODE!')
        print(board.heads)
        goal = min(board.heads, key=lambda f: heuristic((my_head["x"], my_head["y"]), (f["x"], f["y"])))
        print(f'closest Head: {goal}')
        mode = 'hunt'
        next_move_astar = a_star_search((goal["x"], goal["y"]), board, mode)
    elif len(board.food) != 0:
        print(f'FOOD MODE!')
        print(food)
        goal = min(food, key=lambda f: heuristic((my_head["x"], my_head["y"]), (f["x"], f["y"])))
        print(f'closes food: {goal}')
        mode = 'food'
        
        sorted_food_distance = sorted(food, key=lambda f: heuristic((my_head["x"], my_head["y"]), (f["x"], f["y"])))
        print(f'sorted_food_distance:\n {sorted_food_distance}')
        heads_sorted_food_distance = sorted(food, key=lambda f: min(heuristic((head["x"], head["y"]), (f["x"], f["y"])) for head in board.heads))
        print(f'heads_sorted_food_distance:\n {heads_sorted_food_distance}')
        next_move_astar = a_star_search((goal["x"], goal["y"]), board, mode)
    
    if len(board.food) == 0:
        next_move_astar = "no_move"

    if next_move_astar == "no_move":
        is_move_safe = simple_safe_moves(board, is_move_safe)
    else:
        is_move_safe = {
            direction: False
            for (direction, _) in is_move_safe.items()
        }

        print(f'\n next_move_astar: \n {next_move_astar}')
        is_move_safe[next_move_astar] = True

        print(f'\n astar_is_move_safe: \n {is_move_safe}')

    # Now Check if the A star move are head collision safe
    is_move_safe = head_collision_safe_moves(board, is_move_safe)
    print(f'\n astar_head_collsion: \n {is_move_safe}')

    # If the move from A star is not head collision safe, do a simple_safe_moves check
    if all(value is False for value in is_move_safe.values()):
        is_move_safe = simple_safe_moves(board, is_move_safe)
        # Now Check if the safe moves by simple_safe_move are head collision safe
        is_move_safe = head_collision_safe_moves(board, is_move_safe)

    #If head_collision leaves no safe move, then use simple safe move without going to food
    if all(value is False for value in is_move_safe.values()):
        is_move_safe = simple_safe_moves(board, is_move_safe)
        direction_values = board.directions_values
        for v, k in direction_values.items():
            if v == 'f_':
                is_move_safe[k] = False

    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(
            f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        next_move = {"move": "down"}
    else:
        # Choose a random move from the safe ones
        next_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
