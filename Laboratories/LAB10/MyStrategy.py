class MyStrategy:
    def __init__(self, opponent, me):
        self.opponent = opponent
        self.me = me
    
    def win_move(self, board, key=None):
        if key is None:
            key=self.me
        # Check for possible winning moves
        for i in range(3):
            row = [board[i][j] for j in range(3)]
            col = [board[j][i] for j in range(3)]
            if row.count(key) == 2 and row.count('-') == 1:
                return i, row.index('-')
            if col.count(key) == 2 and col.count('-') == 1:
                return col.index('-'), i

        diagonal1 = [board[i][i] for i in range(3)]
        diagonal2 = [board[i][2 - i] for i in range(3)]

        if diagonal1.count(key) == 2 and diagonal1.count('-') == 1:
            ind = diagonal1.index('-')
            return ind, ind
        if diagonal2.count(key) == 2 and diagonal2.count('-') == 1:
            ind = diagonal2.index('-')
            return ind, 2 - ind

        return None

    def block_win(self, board):
        # Block the opponent's possible winning moves
        return self.win_move(board, key=self.opponent)

    def fork(self, board):
        # Create a fork opportunity
        fork_moves = {
            (0, 0): [(1, 0), (0, 1)],
            (0, 2): [(1, 2), (0, 1)],
            (2, 0): [(1, 0), (2, 1)],
            (2, 2): [(1, 2), (2, 1)],
            (1, 1): [(0, 0), (0, 2), (2, 0), (2, 2)]
        }
        for pos, moves in fork_moves.items():
            if board[pos[0]][pos[1]] == self.me:
                for move in moves:
                    if board[move[0]][move[1]] == '-':
                        return move
        return None
    
    def block_fork(self, board):
        # Possible fork positions for the opponent
        fork_positions = [
            [(1, 0), (0, 1), (0, 0)],
            [(1, 0), (2, 1), (2, 0)],
            [(1, 2), (0, 1), (0, 2)],
            [(1, 2), (2, 1), (2, 2)],
        ]

        for positions in fork_positions:
            if board[positions[0][0]][positions[0][1]] == self.opponent and \
            board[positions[1][0]][positions[1][1]] == self.opponent and \
            board[positions[2][0]][positions[2][1]] == '-':
                return positions[2][0], positions[2][1]

        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for corner in corners:
            if board[corner[0]][corner[1]] == self.opponent:
                opp_corners = [(0, 2), (2, 0), (2, 2), (0, 0)]
                for opp_corner in opp_corners:
                    if board[opp_corner[0]][opp_corner[1]] == '-':
                        return opp_corner[0], opp_corner[1]

        return None

    def make_move(self, board):
        strategies = [self.win_move, self.block_win, self.fork, self.block_fork]
        for strategy in strategies:
            move = strategy(board)
            if move:
                return move