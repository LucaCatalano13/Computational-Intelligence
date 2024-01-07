import pygame
import sys

from game import Game, Player, Move
from copy import deepcopy

# Constants
WIDTH, HEIGHT = 505, 505  # Adjusted to fit the lines properly

ROWS, COLS = 5, 5
CELL_SIZE = WIDTH // COLS
LINE_WIDTH = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)

class GameUI(Game):
    def __init__(self, screen) -> None:
        super().__init__()
        self.screen = screen
        self._board_memory = None
    
    def __draw_board(self):
        self.screen.fill(WHITE)
        # Draw vertical lines between the squares
        for i in range(1, COLS):
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        # Draw horizontal lines between the squares
        for i in range(1, ROWS):
            pygame.draw.line(self.screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        # Draw X and O marks
        for row in range(ROWS):
            for col in range(COLS):
                mark = self._board[row][col]
                if mark == 0:
                    pygame.draw.line(self.screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20),
                                    ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), 3)
                    pygame.draw.line(self.screen, RED, ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20),
                                    (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20), 3)
                elif mark == 1:
                    pygame.draw.circle(self.screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                    CELL_SIZE // 2 - 20, 3)
                elif mark in [ord('T'), ord('B'), ord('L'), ord('R')]:
                    pygame.draw.rect(self.screen, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    if self._board_memory[row][col] == 0:
                        pygame.draw.line(self.screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20),
                                    ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), 3)
                        pygame.draw.line(self.screen, RED, ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20),
                                        (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20), 3)
                    if self._board_memory[row][col] == 1:
                        pygame.draw.circle(self.screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                        CELL_SIZE // 2 - 20, 3)

    def __reset_board(self, from_pos):
        self._board[0, from_pos[0]] = self._board_memory[0, from_pos[0]]
        self._board[4, from_pos[0]] = self._board_memory[4, from_pos[0]]
        self._board[from_pos[1], 0] = self._board_memory[from_pos[1], 0]
        self._board[from_pos[1], 4] = self._board_memory[from_pos[1], 4]
    
    def __choose_slide(self, from_pos):
        possible_slide = self.possible_slide((from_pos[1], from_pos[0]))
        if possible_slide is None:
            return None
        self._board_memory = deepcopy(self._board)
        if Move.TOP in possible_slide:
            self._board[0, from_pos[0]] = ord('T')
        if Move.BOTTOM in possible_slide:
            self._board[4, from_pos[0]] = ord('B')
        if Move.LEFT in possible_slide:
            self._board[from_pos[1], 0] = ord('L')
        if Move.RIGHT in possible_slide:
            self._board[from_pos[1], 4] = ord('R')
        self.__draw_board()
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit Pygame
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col, row = pygame.mouse.get_pos()
                    row = row // CELL_SIZE; col = col // CELL_SIZE
                    if self._board[row, col] == ord('T'):
                        self.__reset_board(from_pos)
                        return Move.TOP
                    elif self._board[row, col] == ord('B'):
                        self.__reset_board(from_pos)
                        return Move.BOTTOM
                    elif self._board[row, col] == ord('L'):
                        self.__reset_board(from_pos)
                        return Move.LEFT
                    elif self._board[row, col] == ord('R'):
                        self.__reset_board(from_pos)
                        return Move.RIGHT
            self.__draw_board()
            pygame.display.flip()
    
    def play(self, player1: Player, player2: Player) -> int:
        '''Play the game. Returns the winning player'''
        players = [player1, player2]
        winner = -1
        self.current_player_idx = 0
        while  True:
            # Human player
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit Pygame
                    pygame.quit()
                    sys.exit()
                if winner < 0 and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_player_idx == 0:
                        row, col = pygame.mouse.get_pos()
                        row = row // CELL_SIZE; col = col // CELL_SIZE
                        from_pos = (row, col)
                        # choose the slide
                        slide = self.__choose_slide(from_pos)
                        if slide is None:
                            print("Mossa non valida")
                            continue
                        print(slide)
                        ok = self.move(from_pos, slide, self.current_player_idx)
                        if ok:
                            self.current_player_idx = 1
                            winner = self.check_winner()
                        else:
                            print("Mossa non valida")

            # No human player
            if self.current_player_idx == 1 and winner < 0:
                ok = False
                while not ok:
                    from_pos, slide = players[self.current_player_idx].make_move(self)
                    ok = self.move(from_pos, slide, self.current_player_idx)
                self.current_player_idx = 0
                winner = self.check_winner()
            self.__draw_board()
            pygame.display.flip()
            
            if winner >= 0:
                break

        return winner
        '''Slide the other pieces'''
        # define the corners
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position is not in a corner
        if from_pos not in SIDES:
            # if it is at the TOP, it can be moved down, left or right
            acceptable_top: bool = from_pos[0] == 0 and (
                slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is at the BOTTOM, it can be moved up, left or right
            acceptable_bottom: bool = from_pos[0] == 4 and (
                slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is on the LEFT, it can be moved up, down or right
            acceptable_left: bool = from_pos[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT
            )
            # if it is on the RIGHT, it can be moved up, down or left
            acceptable_right: bool = from_pos[1] == 4 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT
            )
        # if the piece position is in a corner
        else:
            # if it is in the upper left corner, it can be moved to the right and down
            acceptable_top: bool = from_pos == (0, 0) and (
                slide == Move.BOTTOM or slide == Move.RIGHT)
            # if it is in the lower left corner, it can be moved to the right and up
            acceptable_left: bool = from_pos == (4, 0) and (
                slide == Move.TOP or slide == Move.RIGHT)
            # if it is in the upper right corner, it can be moved to the left and down
            acceptable_right: bool = from_pos == (0, 4) and (
                slide == Move.BOTTOM or slide == Move.LEFT)
            # if it is in the lower right corner, it can be moved to the left and up
            acceptable_bottom: bool = from_pos == (4, 4) and (
                slide == Move.TOP or slide == Move.LEFT)
        # check if the move is acceptable
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        # if it is
        if acceptable:
            # take the piece
            piece = self._board[from_pos]
            # if the player wants to slide it to the left
            if slide == Move.LEFT:
                # for each column starting from the column of the piece and moving to the left
                for i in range(from_pos[1], 0, -1):
                    # copy the value contained in the same row and the previous column
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], i - 1)]
                # move the piece to the left
                self._board[(from_pos[0], 0)] = piece
            # if the player wants to slide it to the right
            elif slide == Move.RIGHT:
                # for each column starting from the column of the piece and moving to the right
                for i in range(from_pos[1], self._board.shape[1] - 1, 1):
                    # copy the value contained in the same row and the following column
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], i + 1)]
                # move the piece to the right
                self._board[(from_pos[0], self._board.shape[1] - 1)] = piece
            # if the player wants to slide it upward
            elif slide == Move.TOP:
                # for each row starting from the row of the piece and going upward
                for i in range(from_pos[0], 0, -1):
                    # copy the value contained in the same column and the previous row
                    self._board[(i, from_pos[1])] = self._board[(
                        i - 1, from_pos[1])]
                # move the piece up
                self._board[(0, from_pos[1])] = piece
            # if the player wants to slide it downward
            elif slide == Move.BOTTOM:
                # for each row starting from the row of the piece and going downward
                for i in range(from_pos[0], self._board.shape[0] - 1, 1):
                    # copy the value contained in the same column and the following row
                    self._board[(i, from_pos[1])] = self._board[(
                        i + 1, from_pos[1])]
                # move the piece down
                self._board[(self._board.shape[0] - 1, from_pos[1])] = piece
        return acceptable