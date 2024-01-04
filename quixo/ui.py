import random
import pygame

from  game import Move, Player
from GameUI import GameUI

# Constants
WIDTH, HEIGHT = 505, 505  # Adjusted to fit the lines properly
ROWS, COLS = 5, 5
CELL_SIZE = WIDTH // COLS

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, gameUI: 'GameUI') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, gameUI: 'GameUI') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

class HumanPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, gameUI: 'GameUI') -> tuple[tuple[int, int], Move]:
        row, col = input("Enter the position of the piece you want to move (format r c): ").split()
        row = int(row); col = int(col)
        while row < 0 or row > 4 or col < 0 or col > 4:
            print("Invalid position. Please try again.")
            row, col = int(input("Enter the position of the piece you want to move (format r c): ").split())
        from_pos = (row, col)
        move = input("Enter the direction you want to move the piece (format t, b, l, r): ")
        while move not in ["t", "b", "l", "r"]:
            print("Invalid direction. Please try again.")
            move = input("Enter the direction you want to move the piece (format t, b, l, r): ").split()
        move = Move.TOP if move == "t" else Move.BOTTOM if move == "b" else Move.LEFT if move == "l" else Move.RIGHT
        return from_pos, move

if __name__ == '__main__':
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Quixo Game')
    g = GameUI(screen)
    player1 = HumanPlayer()
    player2 = RandomPlayer()
    
    # Play the game
    winner = g.play(player1, player2)
    print(f"Winner: Player {winner}")
