# AoC
[AoC](https://adventofcode.com/) solutions

TODO:
- find better solution to puzzle 5 (almanac, ranges)
- solve day 12 puzzle part 2 (spring arrangements)
- solve day 17 puzzle (try 3D Dijkstra's algorithm)
- solve day 20 puzzle part 2 (flip-flops and NANDs)
- solve day 21 puzzle part 2 (number of possible end positions)
- solve day 23 puzzle part 2 (longest path without slopes)
- solve day 24 puzzle part 2 (intersecting lines)

Testing performance:
```py
import timeit
n = 1000
x = timeit.timeit(lambda: solver('input', ...), number=n)
print(x / n)
```

Profiling:
```py
import cProfile
cProfile.run("solver('input', ...)")
```
