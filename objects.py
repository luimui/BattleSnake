import numpy as np
import typing

class Board:

  def __init__(self, game_state: typing.Dict):

    self.snakes = game_state["board"]['snakes']
    self.board_game_state = game_state["board"]
    self.food = game_state["board"]['food']


    # Create empty board, padded by walls
    self.board = np.empty([self.board_game_state['height'] + 2, self.board_game_state['width'] + 2], dtype='U10')
    self.board[:,[0,-1]] = 'w_'
    self.board[[0,-1],:] = 'w_'

    # Place food on board
    for i in range(len(self.food)):
      self.board[self.food[i]['x'] + 1, self.food[i]['y'] + 1] = 'f_'

    # Place snakes on board
    for i in range(len(self.snakes)):
      for j in range(len(self.snakes[i]['body'])):
        self.board[self.snakes[i]['body'][j]['x'] + 1 , self.snakes[i]['body'][j]['y'] + 1] = 'b' + str(i)
      self.board[self.snakes[i]['head']['x'] + 1, self.snakes[i]['head']['y'] +1 ] = 'h' + str(i)

    self.board[self.board == ''] = '__'

    #self.board = np.flip(self.board, 0)

    self.head = game_state["board"]['snakes'][0]['head']
    self.directions = {
                        "up":     self.board[(self.head['x'] + 1 )   , (self.head['y'] + 1 + 1)],
                        "down":   self.board[(self.head['x'] + 1 )   , (self.head['y'] + 1 - 1)],
                        "left":   self.board[(self.head['x'] + 1 - 1), (self.head['y'] + 1 )],
                        "right":  self.board[(self.head['x'] + 1 + 1), (self.head['y'] + 1 )]
                      }
