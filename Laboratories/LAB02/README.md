Lab2 done with [Claudio Savelli](https://github.com/ClaudioSavelli)!

# Task

Write agents able to play [*Nim*](https://en.wikipedia.org/wiki/Nim), with an arbitrary number of rows and an upper bound $k$ on the number of objects that can be removed in a turn (a.k.a., *subtraction game*).

The goal of the game is to **avoid** taking the last object.

* Task2.1: An agent using fixed rules based on *nim-sum* (i.e., an *expert system*)
* Task2.2: An agent using evolved rules using ES

# Task2.1

## Methods 

### Optimal Solution 

The `nim_sum` function takes a Nim object and calculates the Nim sum, which is a crucial concept in Nim strategy. It converts the rows to a binary representation and calculates the bitwise XOR of these binary representations to determine the Nim sum.

The `analyze` function analyzes the possible moves in the current game state. It returns a dictionary containing the possible moves and their corresponding Nim sums.

The `optimal` function selects an optimal move from the possible moves by analyzing the Nim sums. It tries to find a move that results in a Nim sum of zero if possible. If no such move exists, it selects a move at random. this function is not optimised on the end-game, where the rule applied is different. 

The `expert_system` function is exactly like the `optimal` one, but it is optimised on the end-game, assuring a winrate of 100%. 

### Other Solutions to evaluate the Optimal one

The `random` function selects a random move from the possible moves.

The `gabriele` function aims to always pick the maximum possible number of objects from the lowest row.

### Play Games

The `play` function plays a game of Nim between two agents. It takes two agent functions as arguments and returns the winning agent.

# Task2.2

## Our Solutions

Two different solutions were developed for this lab:

The first solution implements, as requested, an evolutionary algorithm. 

The second solution instead is based on a MonteCarlo-style algorithm, which we felt could be applied very well to this type of problem, having few 'legal' moves available and not knowing the game principles behind Nim making it difficult to create a suitable fitness function. 


## Evolutionary Strategy

Developing the evolutionary strategy was not easy, considering the fact that we had to write functions that, given a state of the board, would perform a certain well-defined move. Having no knowledge of the game and how to evaluate a board state, some sub-optimal functions were written to test the evolutionary method anyway. 

Various methods are considered within the evolutionary strategy, in particular: 

* `lowest_available`: the stick from the row where there are least available is taken. 

* `mirror_move`: mirrors the opponent's last move. 

* `greedy_move`: Pick the move that minimises the number of sticks in the heap.

* `gabriele`, `optimal`, `expert_system`: Already described before.

Three of these proposed methods are selected within an evolutionary strategy. The game state is divided into three different phases, ealry-game, mid-game and late-game, depending on how many sticks are left in the heap compared to how many we had at the beginning of the game. For each of these phases, we evaluated the probability with which each of the three methods is selected through the evolutionary strategy. 

Considering the non-optimality of the methods proposed by us, we wanted to try to include `optimal` and `expert_system` among the possible methods, imagining that our genetic strategy will always choose the latter two as they are the ones that ensure victory. 


## MonteCarlo Strategy

In the MonteCarlo strategy, the principle followed is as follows: 

Whenever a move is to be made by our player, the latter copies the current board state, and simulates num_matches on the latter. Particularly in simulated games, both players make random moves. For each simulated game, the first move is taken and an evaluation is made as to whether that game is a winner or not. Then the win_ratio is calculated for each available first move made, and the first move that resulted in the most wins is selected.

# Results

## Evolutionary Strategy
Three different combinations of methods were tested: 

* ES1: `lowest_available`, `greedy_move`, `gabriele`
* ES2: `lowest_available`, `greedy_move`, `optimal`
* ES3: `lowest_available`, `greedy_move`, `expert_system`

| ES1 | Winrate |
|-----------|-------|
| Random    | 0.41  |
| Gabriele  | 0.69  |
| Optimal   | 0.33  |

| ES2 | Winrate |
|-----------|-------|
| Random    | 0.63  |
| Gabriele  | 0.71  |
| Optimal   | 0.43  |

| ES3 | Winrate |
|-----------|-------|
| Random    | 0.65  |
| Gabriele  | 0.71  |
| Optimal   | 0.54  |

## MonteCarlo Strategy

| Montecarlo | Winrate |
|-----------|-------|
| Random    | 0.93  |
| Gabriele  | 0.95  |
| Optimal   | 0.88  |

## Evolutionary Strategy vs. MonteCarlo Strategy

| Montecarlo | Winrate |
|-----------|-------|
| ES1 | 0.05 |
| ES2 | 0.06 |
| ES3 | 0.15 |


# Conclusions
The outcomes detail the implementation of diverse approaches in the game of Nim. Evolutionary strategies, denoted as ES1, ES2, and ES3, were employed with varying combinations of move selection methods. Notably, ES3, which integrates an expert_system, falls short of achieving the optimal strategy outlined in task 2.1 and lags behind the effectiveness demonstrated by the Monte Carlo strategy.

The Monte Carlo Strategy stands out for its remarkable performance, consistently attaining high win rates across all scenarios. Its superiority is evident as it consistently outperforms both casual play and specific strategies such as Gabriel and Optimal. This underscores the strategy's efficacy in navigating the intricacies of the Nim game.

The final experiment highlights the near-universal success of the Monte Carlo strategy when pitted against the Evolutionary Strategy. This further emphasizes the potency of the Monte Carlo approach in outperforming alternative strategies, including those driven by evolutionary algorithms.