import random
from MyStrategy import MyStrategy

class Teacher:
    def __init__(self, level=0.9):
        self.ability_level = level
        self.my_strategy = MyStrategy(opponent='O', me='X')

    def random(self, board):
        possibles = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    possibles += [(i, j)]
        return possibles[random.randint(0, len(possibles)-1)]
   
    def make_move(self, board):
        if random.random() > self.ability_level:
            return self.random(board)
        
        move = self.my_strategy.win_move(board)
        if move is not None:
            return move
        
        return self.random(board)