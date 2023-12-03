# Lab09

## ISOLATED ISLANDS

**First experiment: fixed number of generations to swap among islands**

| METHODS         | NO MEMOIZATION |                 | MEMOIZATION     |                 |
|-----------------|----------------|-----------------|-----------------|-----------------|
|| SCORE FITNESS   | GENERATIONS    | SCORE FITNESS   | GENERATIONS    |                 |
| ISLANDS RANDOM  | 0.554          | 60100           | 0.534           | 10462           |
| ISLANDS RING    | 0.598          | 60100           | 0.53            | 5975            |
| ISLANDS FITNESS | 0.508          | 60100           | 0.52            | 54433           |


**Second experiment: when fitnesses are too similar, swap among islands**

| METHODS         | NO MEMOIZATION |                 | MEMOIZATION     |                 |
|-----------------|----------------|-----------------|-----------------|-----------------|
|| SCORE FITNESS   | GENERATIONS    | SCORE FITNESS   | GENERATIONS    |
| ISLANDS RANDOM | 0.526       | 60100       | 0.562       | 3740        |
| ISLANDS RING   | 0.54        | 60100       | 0.533       | 16484       |
| ISLANDS FITNESS| 0.536       | 60100       | 0.516       | 2989        |
