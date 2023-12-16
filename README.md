# AoC
[AoC](https://adventofcode.com/) solutions

TODO:
- solve day 12 part 2
- find better solution to puzzle 5

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
