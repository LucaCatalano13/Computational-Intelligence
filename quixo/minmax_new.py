import numpy as np
import copy
import math
import collections

from game import Game, Player, Move
from QuixoGameLogicWrapper import GameLogicWrapper

class MinMaxPlayer(Player):
    def __init__(self, depth):
        Player.__init__(self)
        self.depth = depth

    def make_move(self, game: 'Game'):
        g = GameLogicWrapper()
        g.set_state(game.get_board())
        g.current_player_idx = game.get_current_player()
        move = self.alphabeta(g, -math.inf, math.inf, self.depth)[1]
        from_pos, slide = move
        for m in Move:
            if m.value == slide.value:
                slide = m
                break
        return from_pos, slide

    def alphabeta(self, game: 'GameLogicWrapper', alpha, beta, depth):
        if (game.check_winner() != -1 or depth == 0):
            score = self._evaluate(game, depth)
            return (score, None)

        depth -= 1
        best_move = None

        possible_moves = game.get_possible_moves()
        move_values = np.ndarray(shape=(len(possible_moves), ))
        for i, move in enumerate(possible_moves):
            # sort possible moves evaluated by the heuristic
            game_copy = copy.deepcopy(game)
            game_copy.move(move[0], move[1], game_copy.get_current_player())
            move_values[i] = self._evaluate(game_copy, depth)
        
        ix_sorted_move_values = move_values.argsort()
        if (game.get_current_player() == 0):
            ix_sorted_move_values = ix_sorted_move_values[::-1]
        ordered_possible_moves = [possible_moves[i] for i in ix_sorted_move_values]
        # ordered_possible_moves = possible_moves

        if (game.get_current_player() == 0):
            for iter, move in enumerate(ordered_possible_moves):
                game_copy = copy.deepcopy(game)
                game_copy.move(move[0], move[1], game_copy.get_current_player())
                val = self.alphabeta(game_copy, alpha, beta, depth)[0]
                if (val > alpha):
                    alpha = val
                    best_move = move
                if (alpha >= beta):
                    break
            return (alpha, best_move)
        else:
            for iter, move in enumerate(ordered_possible_moves):
                game_copy = copy.deepcopy(game)
                game_copy.move(move[0], move[1], game_copy.get_current_player())
                val = self.alphabeta(game_copy, alpha, beta, depth)[0]
                if (val < beta):
                    beta = val
                    best_move = move
                if (alpha >= beta):
                    break
            return (beta, best_move)

    def _find_occurence(self, state, key):
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

    # Evaluates the current game state
    def _evaluate(self, game: 'Game', depth):
        # if game.check_winner() == 0:  # Maximizer won (X)
        #     return 100 + depth
        # elif game.check_winner() == 1:  # Minimizer Won (O)
        #     return -100 - depth  
        # else:
        #     value = 0
        #     occurence_value = self._find_occurence(game.get_board(), game.get_current_player()) * 5

        #     if game.get_board()[2,2] == 1:
        #         value += 20
        #     elif game.get_board()[2,2] == 0:
        #         value -= 20

        #     if game.get_current_player() == 0:
        #         occurence_value *= -1

        #     frequency = np.unique(game.get_board(), return_counts=True)
        #     len_frequency = len(frequency[0])
        #     if len_frequency == 3:
        #         max_piece_count = frequency[1][1]
        #         min_piece_count = frequency[1][2]
        #     elif len_frequency > 1:
        #         max_piece_count = frequency[1][0]
        #         min_piece_count = frequency[1][1]

        #     value += (max_piece_count - min_piece_count) + occurence_value
        #     return value
        transpose = game.get_board().transpose()
        count = []
        opponent_count = []
        for row, column in zip(game.get_board(), transpose):
            row_counter = collections.Counter(row)
            column_counter = collections.Counter(column)
            count.append(row_counter.get(0, 0))
            count.append(column_counter.get(0, 0))
            opponent_count.append(row_counter.get(1, 0))
            opponent_count.append(column_counter.get(1 , 0))

        element_in_codiagonal = game.get_board()[:, ::-1]
        diagonals = [np.diagonal(game.get_board()), np.diagonal(element_in_codiagonal)]
        main_diagonal_count = collections.Counter(diagonals[0])
        second_diagonal_count = collections.Counter(diagonals[1])
        count.append(main_diagonal_count.get(0, 0))
        count.append(second_diagonal_count.get(0, 0))
        opponent_count.append(main_diagonal_count.get(1, 0))
        opponent_count.append(second_diagonal_count.get(1, 0))

        score_max = 5 ** max(count)
        score_min = 5 ** max(opponent_count)

        return score_max - score_min