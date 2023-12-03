
import random
import numpy as np

def roulette(parents, parents_evals):
    if (max(parents_evals)-min(parents_evals)) > 1e-5:
        probabilities = [(score-min(parents_evals)) / (max(parents_evals)-min(parents_evals)) for score in parents_evals]
    else:
        probabilities = [1 for score in parents_evals]
    probabilities = np.array(probabilities)/sum(probabilities)
    p1 = random.choices(parents, k=1, weights=probabilities)[0]
    p2 = random.choices(parents, k=1, weights=probabilities)[0]
            
    return p1, p2