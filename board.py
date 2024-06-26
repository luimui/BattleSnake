import numpy as np
import typing


class Board:
'''Diese Klasse repräsentiert das Spielfeld. Aus dem game_state dict Objekt wird ein NumpyArray erzeugt, und die Objekte dese Spiels (Wände, Snakes, Futter) mit Strings dargestellt. Zusätzlich bietet die Klasse Funktionen an um die Boardinhalte und Koordinaten für jedes Feld des Boards auszugeben.

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


D'''
  def __init__(self, game_state: typing.Dict):

    self.snakes = game_state["board"]['snakes']
    self.board_game_state = game_state["board"]
    self.food = game_state["board"]['food']
    self.head = game_state["you"]["head"]

    # Create empty board, padded by walls
    self.board = np.empty([
      self.board_game_state['height'] + 2, self.board_game_state['width'] + 2
    ],
                          dtype='U10')
    self.board[0, 0] = 'w_'
    self.board[0, -1] = 'w_'
    self.board[-1, 0] = 'w_'
    self.board[-1, -1] = 'w_'

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
        #if j == len(self.snakes[i]['body']) - 1:
        #  self.board[self.snakes[i]['body'][j]['x'] + 1, self.snakes[i]['body'][j]['y'] + 1] = 't' + str(i)

    
    self.board[self.head['x'] + 1, self.head['y'] + 1] = '**'

    self.board[self.board == ''] = '__'

    #self.board = np.flip(self.board, 0)

    self.directions_values = {
      "up": self.board[(self.head['x'] + 1), (self.head['y'] + 1 + 1)],
      "down": self.board[(self.head['x'] + 1), (self.head['y'] + 1 - 1)],
      "left": self.board[(self.head['x'] + 1 - 1), (self.head['y'] + 1)],
      "right": self.board[(self.head['x'] + 1 + 1), (self.head['y'] + 1)]
    }
    self.directions_coordinates = {
      "up": ((self.head['x']), (self.head['y'] + 1)),
      "down": ((self.head['x']), (self.head['y'] - 1)),
      "left": ((self.head['x'] - 1), (self.head['y'])),
      "right": ((self.head['x'] + 1), (self.head['y']))
    }

  def directions_values_for_node(self, nodeX, nodeY):

    return {
      "up": self.board[(nodeX + 1), (nodeY + 1 + 1)],
      "down": self.board[(nodeX + 1), (nodeY + 1 - 1)],
      "left": self.board[(nodeX + 1 - 1), (nodeY + 1)],
      "right": self.board[(nodeX + 1 + 1), (nodeY + 1)]
    }

  def directions_coordinates_for_node(self, nodeX, nodeY):
    return {
      "up": ((nodeX), (nodeY + 1)),
      "down": ((nodeX), (nodeY - 1)),
      "left": ((nodeX - 1), (nodeY)),
      "right": ((nodeX + 1), (nodeY))
    }

  def directions_coordinates_for_direction(self, direction_string, nodeX,
                                           nodeY):

    if direction_string == "up":
      coordinates = (nodeX, nodeY + 1)
    elif direction_string == "down":
      coordinates = (nodeX, nodeY - 1)
    elif direction_string == "left":
      coordinates = (nodeX - 1, nodeY)
    elif direction_string == "right":
      coordinates = (nodeX + 1, nodeY)

    return coordinates

  def get_board_as_list(self):
    return list(np.array(self.board).tolist())
