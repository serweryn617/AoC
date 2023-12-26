# AoC
[AoC](https://adventofcode.com/) solutions

<!--
Result: 42 stars without help from Reddit :)
- Day 17: solved after looking through solutions on MEGATHREAD
  and finding a bug in my visited tiles processing. Solving without
  this fix would take a lot longer, but was probably still possible.
- Day 20 part 2: solved after taking some assumptions about the input
  data, taken from MEGATHREAD
- Day 12 part 2: dynamic programming solution taken from MEGATHREAD
 -->

TODO:
- find better solution to puzzle 5 (almanac, ranges)
- find solution other than DP to day 12 puzzle part 2 (spring arrangements)
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
