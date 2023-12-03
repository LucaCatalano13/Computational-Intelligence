import numpy as np
import random

def one_bit_flip(ind, size=1, mutation_probability=1):
    if random.random() < mutation_probability:
        index = np.random.choice(list(range(len(ind))), size=size, replace=False)
        ind[index] = 1 - ind[index]
    return ind

def mutate_all(ind, p_complete_mutation):
    '''
    Can be merged into one_bit_flip by introducing a for in the previous
    '''
    for idx in range(len(ind)):
        if random() < p_complete_mutation:
            ind[idx] = 1 - ind[idx]
    return ind