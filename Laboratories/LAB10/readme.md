# Tic-Tac-Toe Reinforcement Learning

This lab focuses on training an AI agent to play Tic-tac-toe using reinforcement learning, employing the Q-learning RL algorithm. You have the option to teach the agent by playing against it or using an automated teacher agent.

## Code Structure

- **Training Process:** The agent is trained using a teacher agent (`Teacher.py`) aware of a random strategy and `MyStartegy.py`, which attempts to create multiple possible winning scenarios. However, the teacher only follows this strategy with a certain probability, termed "ability", at each turn.
  
- **Initialization:** Q values for the learning agent are initialized using default dictionaries with values set to 0, ensuring every state-action pair begins with this default value.

- **Implementation Details:** 
  - `Agent.py` houses the Q-learning implementation.
  - `Game.py` contains the main game class, maintaining the state of each game instance and hosting most of the core game functionalities, including the primary game loop within the `play_game()` function.
  
- **Training Process Execution:** 
  - Use the `play.py` script to train the agent. The `GameLearner` class oversees the game sequence, continuing until the player decides to stop or the teacher finishes the designated number of episodes.

## Training a New Agent with the Teacher

To initialize a new RL agent and automatically train it using a teacher agent, employ the `-t` flag followed by the desired number of game iterations for training. Specify the pickle path using the `-p` option.

```bash
python3 play.py -p "name_file.pkl" -t 5000
```

## Automated Agent Testing

Utilize `lab10.ipynb` to test the pre-trained agent, allowing it to play automatically in addition to running 1000 different random plays. Additionally, there's an option for you to play against the agent.