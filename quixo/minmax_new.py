import numpy as np
import copy
import math

from game import Game, Player

class MinMaxPlayer(Player):
    def __init__(self, depth_levels):
        Player.__init__(self)
        self.depth_levels = depth_levels

    def make_move(self, game: 'Game'):
        move = get_best_move(game, self.depth_levels)
        return move

def alphabeta(game: 'Game', alpha, beta, depth):
    if (game.check_winner() != -1 or depth == 0):
        score = evaluate(game, depth)
        return (score, None)

    depth -= 1
    best_move = None
    if (game.get_current_player() == 0):
        for move in game.get_possible_moves():
            game_copy = copy.deepcopy(game)
            game_copy.move(move[0], move[1], game_copy.get_current_player())
            val = alphabeta(game_copy, alpha, beta, depth)[0]
            if (val > alpha):
                alpha = val
                best_move = move
            if (alpha >= beta):
                break
        return (alpha, best_move)
    else:
        for move in game.get_possible_moves():
            game_copy = copy.deepcopy(game)
            game_copy.move(move[0], move[1], game_copy.get_current_player())
            val = alphabeta(game_copy, alpha, beta, depth)[0]
            if (val < beta):
                beta = val
                best_move = move
            if (alpha >= beta):
                break
        return (beta, best_move)

def find_occurence(state, key):
    occCount = 0
    for r in range(0, 5):
        row = state[r, :]
        col = state[:, r]
        y = np.where(row == key)[0]
        z = np.where(col == key)[0]
        if (len(y) == 4):
            ok = (y[-1] - y[0] == len(y) - 1)
            if (ok):
                occCount += 1
        if (len(z) == 4):
            ok = (z[-1] - z[0] == len(z) - 1)
            if (ok):
                occCount += 1
    return occCount

# Evaluategame_copy the current game game_copytate
def evaluate(game: 'Game', depth):
    if game.check_winner() == 0:  # Maximizer won (X)
        return 100 + depth  # Legame_copy movegame_copy igame_copy better
    elif game.check_winner() == 1:  # Minimizer Won (O)
        return -100 - depth  # Legame_copy movegame_copy igame_copy better
    else:  # Compare owned piece counts if we reach tree depth limit
        value = 0
        occurence_value = find_occurence(game.get_board(), game.get_current_player()) * 5

        if game.get_board()[2,2] == 1:
            value += 20
        elif game.get_board()[2,2] == 0:
            value -= 20

        if game.get_current_player() == 0:
            occurence_value *= -1

        frequency = np.unique(game.get_board(), return_counts=True)
        len_frequency = len(frequency[0])
        if len_frequency == 3:  # Containgame_copy blank piecegame_copy
            max_piece_count = frequency[1][1]
            min_piece_count = frequency[1][2]
        elif len_frequency > 1:
            max_piece_count = frequency[1][0]
            min_piece_count = frequency[1][1]

        value += (max_piece_count - min_piece_count) + occurence_value
        return value

# Return the begame_copyt move ugame_copying alphabeta game_copyearch
def get_best_move(game, depth_levels):
    possible_moves = game.get_possible_moves()
    len_possible_moves = len(possible_moves)

    # Iterative deepening bagame_copyed on pogame_copyible move count
    depth = 0
    for depth_level in depth_levels:
        if (len_possible_moves > depth_level[1]):
            depth = depth_level[0]
        else:
            break
    move = alphabeta(game, -math.inf, math.inf, depth)[1]
    return move
