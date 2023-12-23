import numpy as np

class Game:
    """ The game class. New instance created for each new game. """
    def __init__(self, agent, teacher=None):
        self.agent = agent
        self.teacher = teacher
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    def __print_board(self):
        for row in self.board:
            print(row)

    # only for test vs radom agent trained with Q-learning
    def __test_random_move(self):
        # get all possible actions
        actions = []
        for row_ix in range(len(self.board)):
            for col_ix in range(len(self.board[0])):
                if self.board[row_ix][col_ix] == '-':
                    actions.append((row_ix, col_ix))
        # choose a random action
        action = actions[np.random.randint(len(actions))]
        return action

    def player_move(self, only_test):
        if self.teacher is not None:
            action = self.teacher.make_move(self.board)
            self.board[action[0]][action[1]] = 'X'
        elif only_test:
            action = self.__test_random_move()
            self.board[action[0]][action[1]] = 'X'
        else:
            self.__print_board()
            while True:
                move = input("Row Col: ")
                try:
                    row, col = int(move[0]), int(move[2])
                except ValueError:
                    print("INVALID INPUT! Please use the correct format.")
                    continue
                if row not in range(3) or col not in range(3) or not self.board[row][col] == '-':
                    print("INVALID MOVE! Choose again.")
                    continue
                self.board[row][col] = 'X'
                break

    def agent_move(self, action):
        self.board[action[0]][action[1]] = 'O'

    def check_win(self, player_sign):
        # col
        for col_ix in range(len(self.board[0])):
            if self.board[0][col_ix] == self.board[1][col_ix] and self.board[1][col_ix] == self.board[2][col_ix] and self.board[0][col_ix] == player_sign:
                return True
        # row
        for row in self.board:
            if row[0] == row[1] and row[1] == row[2] and row[0] == player_sign:
                return True
        # diag
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] == player_sign:
            return True
        # anti-diag
        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] == player_sign:
            return True
    
    def check_draw(self):
        draw = True
        for row in self.board:
            for el in row:
                if el == '-':
                    draw = False
        return draw

    def end(self, key):
        # -1 if the game is still going, 
        # 0 if it is a draw
        # 1 if the player or agent(RL) has won.
        if self.check_win(key):
            if self.teacher is None:
                self.__print_board()
                if key == 'X':
                    print("Player wins!")
                else:
                    print("RL agent wins!")
            return 1
        elif self.check_draw():
            if self.teacher is None:
                self.__print_board()
                print("It's a draw!")
            return 0
        return -1
    
    def play_game(self, player_first, only_test=False):
        # player/teacher
        if player_first:
            self.player_move(only_test)
        
        # agent
        prev_state = get_state(self.board)
        prev_action = self.agent.get_action(prev_state)
        # iterate until game is over
        while True:
            # execute old_action, observe reward and state
            self.agent_move(prev_action)
            check = self.end(key = 'O')
            if not check == -1:
                # game is over. +1 reward if win 0 if draw
                reward = check
                break
            # player/teacher
            self.player_move(only_test)
            check = self.end(key = 'X')
            if not check == -1:
                # game is over. -1 reward if lose 0 if draw
                reward = -1 * check
                break
            else:
                # game continues. 0 reward
                reward = 0
            
            new_state = get_state(self.board)
            new_action = self.agent.get_action(new_state)
            # update Q-values
            self.agent.update(prev_state, new_state, prev_action, new_action, reward)
            # reset "previous" values
            prev_state = new_state
            prev_action = new_action

        self.agent.update(prev_state, None, prev_action, None, reward)
        return True if check == 1 else False
    
    def start(self):
        if self.teacher is not None:
            _ = self.play_game(player_first = np.random.choice([True, False]))

        else:
            while True:
                response = input("Would you like to go first? [y/n]: ")
                print('')
                if response == 'n' or response == 'no':
                    _ = self.play_game(player_first=False)
                    break
                elif response == 'y' or response == 'yes':
                    _ = self.play_game(player_first=True)
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

def get_state(board):
    # the board state into a string key for that state. They are used for Q-value hashing.
    key = ''
    for row in board:
        for elt in row:
            key += elt
    return key