import parser
import os
import pickle
import sys
import numpy as np
import matplotlib.pylab as plt


def plot_agent_reward(rewards):
    plt.plot(np.cumsum(rewards))
    plt.title('Agent Cumulative Reward vs. Iteration')
    plt.ylabel('Reward')
    plt.xlabel('Episode')
    plt.show()


if __name__ == "__main__":
    args = parser.parse_arguments()
    if not os.path.isfile(args.path):
        print("Cannot load agent: file does not exist. Quitting.")
        sys.exit(0)
    with open(args.path, 'rb') as f:
        agent = pickle.load(f)

    plot_agent_reward(agent.rewards)