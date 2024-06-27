import numpy as np
import typing


class Board:
  '''
  Diese Klasse repräsentiert das Spielfeld. Aus dem game_state dict Objekt wird ein NumpyArray als Attribut Board.board erzeugt, und die Objekte dese Spiels (Wände, Snakes, Futter) mit Strings dargestellt. 
('w<x>': Wand, 'h<x>': Kopf von anderer Schlange x, 'b<x>': Körper von Schlange x, '**': eigener Kopf, 'f_': Futter) 
Zusätzlich bietet die Klasse Funktionen an um die Boardinhalte und Koordinaten für jedes Feld des Boards auszugeben.

directions_values_for_node(self, nodeX, nodeY): Gibt die Werte der Nachbarn eines Feldes zurück, erwartet Koordinaten als Parameter. 
{'up': 'f_', 'down': '__', 'left': 'b1', 'right': '__'}

directions_coordinates_for_node(self, nodeX, nodeY): Gibt die Koordinaten der Nachbarn eines Feldes zurück, erwartet Koordinaten als Parameter. 
{"up": (2,2), "down": (2,0), "left": (1,1), "right": (3,1)}

directions_coordinates_for_direction(self, direction_string, nodeX, nodeY): Gibt die Koordinaten der Nachbarn eines Feldes zurück, erwartet eine Richtung und Koordinaten als Parameter. 
{"up": (2,2), "down": (2,0), "left": (1,1), "right": (3,1)}

Das Attribut Board.directions_values gibt die Werte der Nachbarn des eigenen Kopfes zurück.
{'up': 'f_', 'down': '__', 'left': 'b1', 'right': '__'}

Das Attribut Board.directions_coordinates gibt die Koordinaten der Nachbarn des eigenen Kopfes zurück.
{"up": (2,2), "down": (2,0), "left": (1,1), "right": (3,1)}

[['w_' 'w0' 'w1' 'w2' 'w3' 'w4' 'w5' 'w6' 'w7' 'w8' 'w9' 'w10' 'w_']
 ['w10' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' 'w10']
 ['w9' '__' '__' '__' 'f_' '__' '__' '__' '__' 'h0' 'b0' '__' 'w9']
 ['w8' '__' '__' '__' '__' '__' '__' '__' '__' '__' 'b0' 'b0' 'w8']
 ['w7' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' 'w7']
 ['w6' '__' '__' '__' '__' '__' '__' '__' '**' 'b1' '__' '__' 'w6']
 ['w5' '__' '__' '__' '__' 'b1' 'b1' 'b1' 'b1' 'b1' '__' '__' 'w5']
 ['w4' '__' '__' '__' '__' 'b1' '__' '__' '__' '__' '__' '__' 'w4']
 ['w3' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' 'w3']
 ['w2' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' 'w2']
 ['w1' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' 'w1']
 ['w0' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' '__' 'w0']
 ['w_' 'w0' 'w1' 'w2' 'w3' 'w4' 'w5' 'w6' 'w7' 'w8' 'w9' 'w10' 'w_']]

Die Koordinaten sind die (x,y) Werte des Feldes, nicht die (row,col) Werte des NumpyArrays.
'''

  def __init__(self, game_state: typing.Dict):

    self.snakes           = game_state["board"]['snakes']
    self.board_game_state = game_state["board"]
    self.food             = game_state["board"]['food']
    self.head             = game_state["you"]["head"]
    self.length           = game_state['you']['length']
    self.health           = game_state['you']['health']
    

    length_others = []
    for snake in game_state['board']['snakes']:
      if snake['id'] != game_state['you']['id']:
        length_others.append(snake['length'])
      if len(game_state['board']['snakes']) == 1:
        length_others.append(10000)
    self.max_length_others = max(length_others)

    heads = []
    for snake in game_state["board"]['snakes']:
      if snake['id'] != game_state['you']['id']:
        head = snake['head']
        heads.append(head)
    self.heads = heads
    
    # Create empty board, padded by walls
    self.board = np.empty([
      self.board_game_state['height'] + 2, self.board_game_state['width'] + 2
    ],
                          dtype='U10')
    self.board[0, 0]    = 'w_'
    self.board[0, -1]   = 'w_'
    self.board[-1, 0]   = 'w_'
    self.board[-1, -1]  = 'w_'

    self.board[0, :] = np.array(
      ['w_'] +
      ['w' + str(col)
       for col in range(0, self.board_game_state['width'])] + ['w_'])
    self.board[-1, :] = np.array(
      ['w_'] +
      ['w' + str(col)
       for col in range(0, self.board_game_state['width'])] + ['w_'])

    self.board[:, 0] = np.array(
      ['w_'] +
      ['w' + str(col)
       for col in range(0, self.board_game_state['height'])] + ['w_'])
    self.board[:, -1] = np.array(
      ['w_'] +
      ['w' + str(col)
       for col in range(0, self.board_game_state['height'])] + ['w_'])

    # Place food on board
    for i in range(len(self.food)):
      self.board[self.food[i]['x'] + 1, self.food[i]['y'] + 1] = 'f_'

    # Place snakes on board
    for i in range(len(self.snakes)):
      for j in range(len(self.snakes[i]['body'])):
        self.board[self.snakes[i]['body'][j]['x'] + 1, self.snakes[i]['body'][j]['y'] + 1] = 'b' + str(i)
        self.board[self.snakes[i]['head']['x'] + 1, self.snakes[i]['head']['y'] + 1] = 'h' + str(i)
        
    
    self.board[self.head['x'] + 1, self.head['y'] + 1] = '**'

    self.board[self.board == ''] = '__'

   
    self.directions_values = {
      "up": self.board[(self.head['x'] + 1), (self.head['y'] + 1 + 1)],
      "down": self.board[(self.head['x'] + 1), (self.head['y'] + 1 - 1)],
      "left": self.board[(self.head['x'] + 1 - 1), (self.head['y'] + 1)],
      "right": self.board[(self.head['x'] + 1 + 1), (self.head['y'] + 1)]
    }
    '''Gibt die Werte der Nachbarn des eigenen Kopfes zurück.
    {'up': 'f_', 'down': '__', 'left': 'b1', 'right': '__'}'''

    
    self.directions_coordinates =  {
      "up": ((self.head['x']), (self.head['y'] + 1)),
      "down": ((self.head['x']), (self.head['y'] - 1)),
      "left": ((self.head['x'] - 1), (self.head['y'])),
      "right": ((self.head['x'] + 1), (self.head['y']))
    }
    '''Gibt die Koordinaten der Nachbarn des eigenen Kopfes zurück.
    {"up": (2,2), "down": (2,0), "left": (1,1), "right": (3,1)}'''

  def directions_values_for_node(self, nodeX, nodeY):
    '''Gibt die Werte der Nachbarn eines Feldes zurück, erwartet Koordinaten als Parameter. 

    Parameter:
    ----------
    nodeX, nodeY: (x,y) Koordinaten des Feldes

    Return:
    ----------    
    {'up': 'f_', 'down': '__', 'left': 'b1', 'right': '__'}'''
    return {
      "up": self.board[(nodeX + 1), (nodeY + 1 + 1)],
      "down": self.board[(nodeX + 1), (nodeY + 1 - 1)],
      "left": self.board[(nodeX + 1 - 1), (nodeY + 1)],
      "right": self.board[(nodeX + 1 + 1), (nodeY + 1)]
    }

  def directions_coordinates_for_node(self, nodeX, nodeY):
    '''Gibt die Koordinaten der Nachbarn eines Feldes zurück, erwartet Koordinaten als Parameter. 

    Parameter:
    ----------
    nodeX, nodeY: (x,y) Koordinaten des Feldes

    Return:
    ----------
    {"up": (2,2), "down": (2,0), "left": (1,1), "right": (3,1)}'''
    return {
      "up": ((nodeX), (nodeY + 1)),
      "down": ((nodeX), (nodeY - 1)),
      "left": ((nodeX - 1), (nodeY)),
      "right": ((nodeX + 1), (nodeY))
    }

  def directions_coordinates_for_direction(self, direction_string, nodeX,
                                           nodeY):
    '''Gibt die Koordinaten der Nachbarn eines Feldes zurück, erwartet eine Richtung und Koordinaten als Parameter. 

    Parameter:
    ----------
    direction_string: "up", "down", "left", "right"
    nodeX, nodeY: (x,y) Koordinaten des Feldes

    Return:
    ----------
    {"up": (2,2), "down": (2,0), "left": (1,1), "right": (3,1)}'''

    if direction_string == "up":
      coordinates = (nodeX, nodeY + 1)
    elif direction_string == "down":
      coordinates = (nodeX, nodeY - 1)
    elif direction_string == "left":
      coordinates = (nodeX - 1, nodeY)
    elif direction_string == "right":
      coordinates = (nodeX + 1, nodeY)

    return coordinates

