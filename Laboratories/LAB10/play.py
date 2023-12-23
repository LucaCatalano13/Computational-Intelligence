import parser
import os
import pickle
import sys
from tqdm import tqdm

from Agent import Qlearner
from Teacher import Teacher
from Game import Game


class GameLearning(object):
    def __init__(self, args, alpha=0.5, gamma=0.9, epsilon=0.1):
        if args.load:
            if not os.path.isfile(args.path):
                raise ValueError("Cannot load agent: file does not exist.")
            with open(args.path, 'rb') as f:
                agent = pickle.load(f)
        else:
            if os.path.isfile(args.path):
                print('An agent is already saved at {}.'.format(args.path))
                while True:
                    response = input("Are you sure you want to overwrite? [y/n]: ")
                    if response.lower() in ['y', 'yes']:
                        break
                    elif response.lower() in ['n', 'no']:
                        sys.exit(0)
                    else:
                        print("Invalid input. Please choose 'y' or 'n'.")
            agent = Qlearner(alpha, gamma, epsilon)

        self.agent = agent
        self.path = args.path

    def player_mode(self):
        print("You are 'X' and the computer is 'O'.")
        game = Game(self.agent)
        game.start()

    def teacher_mode(self, episodes):
        teacher = Teacher(level=args.ability_level)
        for _ in tqdm(range(episodes)):
            game = Game(self.agent, teacher=teacher)
            game.start()
        # save final agent
        self.agent.save(self.path)


if __name__ == "__main__":
    args = parser.parse_arguments()
    # initialize game instance
    gl = GameLearning(args)
    # play or teach
    if args.teacher_episodes is not None:
        gl.teacher_mode(args.teacher_episodes)
    else:
        gl.player_mode()