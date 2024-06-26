def simple_safe_moves(board, is_move_safe, game_state):
  # Are there any safe moves left?
  safe_moves = []

  directions_values = board.directions_values
  for k,v in directions_values.items():
      if v == '__' or v == 'f_':
          is_move_safe[k] = True
      else:
          is_move_safe[k] = False

  for move, isSafe in is_move_safe.items():
      if isSafe:
          safe_moves.append(move)

  if len(safe_moves) == 0:
      print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
      next_move = {"move": "down"}
  else: 
      # Choose a random move from the safe ones
      next_move = random.choice(safe_moves)


  return next_move