# This program is too slow and doesn't return correct results


import multiprocessing
import random


ALPHA = 2  # Pheromone exponent
BETA = 0.5  # Length exponent
EVAPORATION = 0.99

# Probability modifier for already visited tiles
VISITED = 0.1

CYCLES = 50
ANT_GROUP = 32

FORWARD = {
    'l': (0, -1),
    'r': (0, 1),
    'u': (-1, 0),
    'd': (1, 0),
}


class Ant:
    def __init__(self, y, x, d, ty, tx):
        self.x = x
        self.y = y
        self.d = d
        self.tx = tx
        self.ty = ty
        self.visited = []
        self.straight = 0
        self.heat_loss = 0

    def update_dir(self, grid, pheromone):
        next_tiles = []

        if self.d in ('l', 'r'):
            next_tiles.append((self.y - 1, self.x, 'u'))
            next_tiles.append((self.y + 1, self.x, 'd'))
        elif self.d in ('u', 'd'):
            next_tiles.append((self.y, self.x - 1, 'l'))
            next_tiles.append((self.y, self.x + 1, 'r'))

        if self.straight < 3:
            dy, dx = FORWARD[self.d]
            next_tiles.append((self.y + dy, self.x + dx, self.d))

        next_tiles = self.validate_tiles(next_tiles)
        next_d = self.choose_direction(next_tiles, grid, pheromone)

        if next_d != self.d:
            self.straight = 0

        # print('Dir', self.d, 'Next', next_d)
        self.d = next_d

    def validate_tiles(self, tiles):
        valid_tiles = []

        for y, x, d in tiles:
            if self.ty == y and self.tx == x:
                return [(y, x, d)]

            # Assume the solution doesn't require crossing a single tile twice
            #  and (y, x) not in visited

            if 0 <= y < 13 and 0 <= x < 13:  # TODO
                valid_tiles.append((y, x, d))

        return valid_tiles

    def choose_direction(self, tiles, grid, pheromone):
        probabilities = []

        for y, x, d in tiles:
            p = pheromone[y][x]
            l = grid[y][x]
            probabilities.append(p ** ALPHA / l ** BETA)

            # Discourage crossing the same tile more than once
            if (y, x) in self.visited:
                probabilities[-1] *= VISITED

        rand = random.random()
        total = sum(probabilities)
        # print('probabilities', probabilities)
        # print('    normalize', [i / total for i in probabilities])

        for i in range(len(probabilities)):
            probabilities[i] /= total
            if rand < sum(probabilities[0:i + 1]):
                # print('Rand', rand, 'Prob', sum(probabilities[0:i + 1]))
                return tiles[i][2]

    def move(self, grid):
        dy, dx = FORWARD[self.d]
        self.x += dx
        self.y += dy

        self.straight += 1
        self.visited.append((self.y, self.x))
        self.heat_loss += grid[self.y][self.x]

        # print('Move to', self.x, self.y)

    def reached_end(self):
        # print('Checking', self.x, self.y, '--', self.tx, self.ty)
        return self.ty == self.y and self.tx == self.x


def process_ant(args):
    ant, grid, pheromone = args
    while not ant.reached_end():
        ant.update_dir(grid, pheromone)
        ant.move(grid)

    return ant


def unleash_the_ants(grid, start, end):
    max_y = len(grid)
    max_x = len(grid[0])

    # Initially guide ants to bottom right
    # TODO: guide to the end instead
    # pheromone = [[1 + x + y for x in range(max_x)] for y in range(max_y)]
    pheromone = [[1 for _ in range(max_x)] for _ in range(max_y)]
    min_heat_loss = None

    # print('Pheromone initial')
    # for p in pheromone:
    #     print(p)

    for _ in range(CYCLES):
        print('CYCLE', _)
        ants = [Ant(*start, 'r', *end) for _ in range(ANT_GROUP)]

        # pool = multiprocessing.Pool(32)
        # args = [(ant, grid, pheromone) for ant in ants]
        # ants = pool.map(process_ant, args)

        for i in range(len(ants)):
            while not ants[i].reached_end():
                ants[i].update_dir(grid, pheromone)
                ants[i].move(grid)

        for ant in ants:
            dp = 1 / ant.heat_loss
            for y, x in set(ant.visited):
                pheromone[y][x] += dp

        for y in range(len(pheromone)):
            for x in range(len(pheromone[0])):
                pheromone[y][x] = max(pheromone[y][x] * EVAPORATION, 1)

        losses = [ant.heat_loss for ant in ants]
        ant_heat_loss = min(losses)
        idx = losses.index(ant_heat_loss)

        if min_heat_loss is not None:
            if ant_heat_loss < min_heat_loss:
                min_heat_loss = ant_heat_loss
                best_visited = ants[idx].visited
                print("New best in", _)
            # min_heat_loss = min(min_heat_loss, ant.heat_loss)
        else:
            min_heat_loss = ant_heat_loss
            best_visited = ants[idx].visited

    display_visited(best_visited)

    return min_heat_loss


def display_visited(visited):
    print('Visited:')
    for x in range(13):
        for y in range(13):
            if (y, x) in visited:
                print('X', end='')
            else:
                print('.', end='')
        print()


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        grid = [line.strip() for line in puzzle.readlines()]

    for i in range(len(grid)):
        grid[i] = [int(tile) for tile in grid[i]]

    return grid


def solver(input_path, puzzle_type):
    assert puzzle_type in ('energized', 'max')

    grid = loader(input_path)

    start = 0, 0
    end = len(grid) - 1, len(grid[0]) - 1

    min_heat_loss = unleash_the_ants(grid, start, end)

    return min_heat_loss


def run_examples():
    examples = (
        ('test_input', 'energized', 102),
        # ('test_input', 'max', 51),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'energized')
    # part2 = solver('input', 'max')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    # print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 735ms

    # Regression test
    # assert part1 == 7046
    # assert part2 == 7313


if __name__ == '__main__':
    run_examples()
    # main()
