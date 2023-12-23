import os
import pickle
import collections
import numpy as np
import random

class Qlearner:
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        # agent parameters
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay
        # possible actions
        self.actions = []
        for i in range(3):
            for j in range(3):
                self.actions.append((i,j))
        # Q[a][s]
        self.Q = {}
        for action in self.actions:
            self.Q[action] = collections.defaultdict(int)
        # list of reward received at each episode
        self.rewards = []

    def get_action(self, state):
        # Esempio
        # X - -
        # - - -
        # - - -
        # state = 'X--------'
        # if actions = [(0,0), (0,1), (0,2), (1,0), (1,1), ...]
        # actions[0] = (0,0) = a
        # actions[0][0] = 0
        # 0*3 perchè faccio flatten delle righe quindi 0*3 = 0 1*3 = 3 2*3 = 6 ==> inizio righe
        # actions[0][1] = 0 --> jum colonna ==> uso +
        # state[a[0] * 3 + a[1]] = 'X'
        
        # get possible actions
        possible_actions = [a for a in self.actions if state[a[0]*3 + a[1]] == '-']
        if random.random() < self.eps:
            # Random choose.
            action = possible_actions[random.randint(0,len(possible_actions)-1)]
        else:
            # Greedy choose.
            values = np.array([self.Q[a][state] for a in possible_actions])
            # Find location of max
            ix_max = np.where(values == np.max(values))[0]
            # if multiple max, choose the first one
            ix_select = ix_max[0]
            action = possible_actions[ix_select]
        # update epsilon
        self.eps *= (1.-self.eps_decay)
        return action

    def save(self, path):
        if os.path.isfile(path):
            os.remove(path)
        f = open(path, 'wb')
        pickle.dump(self, f)
        f.close()

    def update(self, prev_state, new_state, prev_action, next_action, reward):
        # update Q(s,a)
        if new_state is not None:
            possible_actions = [action for action in self.actions if new_state[action[0]*3 + action[1]] == '-']
            Q_options = [self.Q[action][new_state] for action in possible_actions]
            # update
            self.Q[prev_action][prev_state] += self.alpha*(reward + self.gamma*max(Q_options) - self.Q[prev_action][prev_state])
        else:
            # terminal state update
            self.Q[prev_action][prev_state] += self.alpha*(reward - self.Q[prev_action][prev_state])
        # add r to rewards list
        self.rewards.append(reward)