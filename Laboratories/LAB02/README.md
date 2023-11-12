Lab2 done with [Claudio Savelli](https://github.com/ClaudioSavelli)!

## Task

Write agents able to play [*Nim*](https://en.wikipedia.org/wiki/Nim), with an arbitrary number of rows and an upper bound $k$ on the number of objects that can be removed in a turn (a.k.a., *subtraction game*).

The goal of the game is to **avoid** taking the last object.

* Task2.1: An agent using fixed rules based on *nim-sum* (i.e., an *expert system*)
* Task2.2: An agent using evolved rules using ES

## Methodology 

### Task2.1

#### Optimal Solution 

The `nim_sum` function takes a Nim object and calculates the Nim sum, which is a crucial concept in Nim strategy. It converts the rows to a binary representation and calculates the bitwise XOR of these binary representations to determine the Nim sum.

The `analyze` function analyzes the possible moves in the current game state. It returns a dictionary containing the possible moves and their corresponding Nim sums.

The `optimal` function selects an optimal move from the possible moves by analyzing the Nim sums. It tries to find a move that results in a Nim sum of zero if possible. If no such move exists, it selects a move at random.

#### Other Solutions to evaluate the Optimal one

The `random` function selects a random move from the possible moves.

The `gabriele` function aims to always pick the maximum possible number of objects from the lowest row.

#### Play Games

The `play` function plays a game of Nim between two agents. It takes two agent functions as arguments and returns the winning agent.

### Task2.2

#### Gaussian Sampling

In our initial approach, we sample NUM_MATCHES matches for each move our agent needs to make. In these matches, our agent randomly selects a move from all available moves following a Gaussian distribution. For each game won, we consider the first move made as the one our agent should choose next. After completing the games, we identify the move that resulted in victory most frequently and select it as the next move.

#### Smart Gaussian Sampling

This code implements a more advanced strategy for playing the Nim game, which combines randomness (Gaussian sampling) with some degree of strategy (prioritizing certain moves). The order strategy can, as possible to see in Results section, influence the move selection in the game.

The function `smart_sort_moves` sorts the possible moves  

#### Methodology

### Results






