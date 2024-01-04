from game import Player
import collections
import numpy as np
import copy

class MinMaxPlayer(Player):
	def __init__(self, depth=2):
		super().__init__()
		self.move = None
		self.depth = depth

	def make_move(self, game):
		gamecopy = copy.deepcopy(game)
		root = TreeNode(gamecopy)
		tree = Tree(root, self.depth)
		minimax = AlphaBeta(tree)
		best_state = minimax.alpha_beta_search(tree.root)
		move = best_state.action
		return move[0], move[1]

class TreeNode:
	def __init__(self, game, action=None, parent=None):
		self.game = game
		self.value = self.evaluate(self.game)
		self.parent = parent
		self.moves = self.game.get_possible_moves()
		self.children = []
		self.action = action # move that leads to this node

	def add_child(self, child):
		if child not in self.children:
			self.children.append(child)

	def expand(self):
		# for each move in the list of possible moves, create a child node and add it to the children list
		for move in self.moves:
			gamecopy = copy.deepcopy(self.game)
			gamecopy.move(move[0], move[1], gamecopy.get_current_player())
			child = TreeNode(gamecopy, move, self)
			self.add_child(child)

	def evaluate(self, game):
		# For every row, column and diagonal it counts the number of X and O and stores in lists.
		# score = 5^(max number of X in all possible rows cols and diag) - 5^(max number of O in all possible rows cols and diag)
		# change X and O if the player is not maximizing player
		transpose = game.get_board().transpose()
		count = []
		opponent_count = []
		for row, column in zip(game.get_board(), transpose):
			row_counter = collections.Counter(row)
			column_counter = collections.Counter(column)
			count.append(row_counter.get(game.get_current_player(), 0))
			count.append(column_counter.get(game.get_current_player(), 0))
			opponent_count.append(row_counter.get(1 - game.get_current_player(), 0))
			opponent_count.append(column_counter.get(1 - game.get_current_player() , 0))

		element_in_codiagonal = game.get_board()[:, ::-1]
		diagonals = [np.diagonal(game.get_board()), np.diagonal(element_in_codiagonal)]
		main_diagonal_count = collections.Counter(diagonals[0])
		second_diagonal_count = collections.Counter(diagonals[1])
		count.append(main_diagonal_count.get(game.get_current_player(), 0))
		count.append(second_diagonal_count.get(game.get_current_player(), 0))
		opponent_count.append(main_diagonal_count.get(1 - game.get_current_player(), 0))
		opponent_count.append(second_diagonal_count.get(1 - game.get_current_player(), 0))

		score_max = 5 ** max(count)
		score_min = 5 ** max(opponent_count)

		return score_max - score_min

class Tree:
	def __init__(self, root, depth):
		self.root = root
		self.depth = depth
		self.expand_tree(self.root, self.depth)
			
	def expand_tree(self, node, depth):
		if depth <= 0:
			return
		node.expand()
		if len(node.children) != 0:
			for child in node.children:
				self.expand_tree(child, depth - 1)

class AlphaBeta:
	def __init__(self, game_tree):
		self.game_tree = game_tree
		self.root = game_tree.root  

	def alpha_beta_search(self, node):
		best_val = -float('inf')
		beta = float('inf')
		best_state = None
		for state in node.children:
			value = self.min_value(state, best_val, beta)
			if value > best_val:
				best_val = value
				best_state = state
		return best_state

	def max_value(self, node, alpha, beta):
		if len(node.children) == 0:
			return node.value
		value = -float('inf')
		for state in node.children:
			value = max(value, self.min_value(state, alpha, beta))
			if value >= beta:
				return value
			alpha = max(alpha, value)
		return value

	def min_value(self, node, alpha, beta):
		if len(node.children) == 0:
			return node.value
		value = float('inf')
		for state in node.children:
			value = min(value, self.max_value(state, alpha, beta))
			if value <= alpha:
				return value
			beta = min(beta, value)
		return value
