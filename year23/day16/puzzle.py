MIRRORS = {
    '/': {'l': 'd', 'r': 'u', 'u': 'r', 'd': 'l'},
    '\\': {'l': 'u', 'r': 'd', 'u': 'l', 'd': 'r'},
}

SPLITTERS = {
    '|': {'l': ('u', 'd'), 'r': ('u', 'd')},
    '-': {'u': ('l', 'r'), 'd': ('l', 'r')},
}


class LightRay:
    def __init__(self, y, x, d):
        self.y = y
        self.x = x
        self.d = d
        self.tile = '.'

    def move(self):
        if self.d == 'l':
            self.x -= 1
        elif self.d == 'r':
            self.x += 1
        elif self.d == 'u':
            self.y -= 1
        elif self.d == 'd':
            self.y += 1

    def update_dir(self, grid):
        self.tile = grid[self.y][self.x]

        if self.tile in MIRRORS:
            self.d = MIRRORS[self.tile][self.d]

        if self.tile in SPLITTERS and self.d in SPLITTERS[self.tile]:
            self.d, new_dir = SPLITTERS[self.tile][self.d]
            return self.y, self.x, new_dir


def edge_generator(max_y, max_x):
    for y in range(max_y):
        yield y, -1, 'r'
        yield y, max_x, 'l'

    for x in range(max_x):
        yield -1, x, 'd'
        yield max_y, x, 'u'


def get_num_energized(grid, rays, max_y, max_x):
    visited = [[[] for _ in range(max_x)] for _ in range(max_y)]

    while rays:
        n = 0
        rays[n].move()

        if (rays[n].x < 0 or rays[n].x >= max_x or
            rays[n].y < 0 or rays[n].y >= max_y or
            rays[n].d in visited[rays[n].y][rays[n].x]
        ):
            rays.pop(n)
            continue

        visited[rays[n].y][rays[n].x].append(rays[n].d)
        split = rays[n].update_dir(grid)
        if split:
            rays.append(LightRay(*split))

    total = 0
    for row in visited:
        total += sum(map(bool, row))

    return total


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        grid = [line.strip() for line in puzzle.readlines()]

    return grid


def solver(input_path, puzzle_type):
    assert puzzle_type in ('energized', 'max')

    grid = loader(input_path)

    max_y = len(grid)
    max_x = len(grid[0])

    if puzzle_type == 'energized':
        rays = [LightRay(0, -1, 'r')]
        total = get_num_energized(grid, rays, max_y, max_x)
        return total
    else:
        energized_max = 0
        for ray_params in edge_generator(max_y, max_x):
            rays = [LightRay(*ray_params)]
            curr = get_num_energized(grid, rays, max_y, max_x)
            energized_max = max(energized_max, curr)
        return energized_max


def run_examples():
    examples = (
        ('test_input', 'energized', 46),
        ('test_input', 'max', 51),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'energized')
    part2 = solver('input', 'max')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.6f}s')  # 800ms

    # Regression test
    assert part1 == 7046
    assert part2 == 7313


if __name__ == '__main__':
    run_examples()
    main()
