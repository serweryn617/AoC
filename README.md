# AoC
[AoC](https://adventofcode.com/) solutions

TODO:
- solve day 17 puzzle (try 3D Dijkstra's algorithm)
- solve day 12 puzzle part 2 (spring arrangements)
- find better solution to puzzle 5 (Almanac, ranges)
- solve day 20 puzzle part 2 (flip-flops and NANDs)

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
