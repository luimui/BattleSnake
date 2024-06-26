import numpy as np

def simple_safe_moves(board, is_move_safe):
    '''
    Diese Methode prüft, ob es noch einen sicheren Zug gibt, d.h. ob die möglichen Richtungen Nahrung oder ein leeres Feld zeigen, aber keine Schlangenköpfe, Körper (einschließlich unserer eigenen) oder Wände. Sie gibt ein aktualisiertes is_move_safe-Wörterbuch zurück, und erwartet als Parameter ein Board-Objekt und ein is_move_safe dict.

    Parameters
    ----------
    board: Board object
    is_move_safe: dict of possible directions

    
    Return:
    ----------
    {'up': False, 'down': True, 'left': False, 'right': False}
    '''
    directions_values = board.directions_values
    for k, v in directions_values.items():
        if v == '__' or v == 'f_':
            is_move_safe[k] = True
        else:
            is_move_safe[k] = False

    return is_move_safe


def head_collision_safe_moves(board, is_move_safe):
    '''Diese Methode prüft, ob sich für die möglichen Richtungen des Kopfes im nächsten Zug auch der Kopf einer anderen Schlange befinden kann. Sollte das der Fall, wird das Feld als False im is_move_safe dict markiert. Sollte unsere Schlange allerdings länger als die andere Schlange sein, bleibt Feld im is_move_safe dict True.
    Sie gibt ein aktualisiertes is_move_safe-Wörterbuch zurück, und erwartet als Parameter ein Board-Objekt und ein is_move_safe dict.
    
    Parameter
    ----------
    board: Board object
    is_move_safe: dict of possible directions


    Return:
    ----------
    {'up': False, 'down': True, 'left': False, 'right': False}
    '''

    #Check only possible safe moves
    for k,v in is_move_safe.items():
        if v == True:
            #Get surrounding field values for those safe moves
            coordinates = board.directions_coordinates_for_direction(k, board.head['x'], board.head['y'])
            directions_values_for_node = board.directions_values_for_node(coordinates[0], coordinates[1])
            
            print(f'\n directions_values_head_collision: \n {directions_values_for_node}')
            
            #Check if there is a head 
            if vales_contain_substring(directions_values_for_node.values(), 'h'):
                #Get Snake number 'h1', 'h2', and check length
                snake_head = search(directions_values_for_node, 'h')
                snake_number = snake_head[-1]
                body_name = ('b' + snake_number)
                snake_length = np.sum(board.board == body_name) + 2
                print(f'\n snake_length: {snake_length}')
                print(f'\n MySnake length: {board.length}')
                #If it is not a shorter snake, move is not safe
                if snake_length >= board.length:
                    is_move_safe[k] = False
                    print(f'is_move_safe[k]: {is_move_safe[k]}')
                    
                
    print(f'head_collision_safe_moves result: \n {is_move_safe}')
    return is_move_safe


def search(dictionary, searchFor):
    for k in dictionary:
        if searchFor in dictionary[k]:
          dictionary[k]
          return dictionary[k]
    return None


def vales_contain_substring(strings, x):
    for s in strings:
        if x in s:
            return True
    return False
