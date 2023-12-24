STEPS = (-3, -2, -1, 1, 2, 3)


class Head:
    def __init__(self, position):
        self.pos = position
        self.length = 0
        self.visited = []

    def sort_key(self):
        return self.length


def display_visited(visited):
    print('Visited:')
    for x in range(13):
        for y in range(13):
            if (y, x) in visited:
                print('X', end='')
            else:
                print('.', end='')
        print()


def get_next_pos(pos, x_limits, y_limits):
    x, y, z = pos

    x_min, x_max = x_limits
    y_min, y_max = y_limits

    if z:
        next_pos = [(x, y + dy, not z) for dy in STEPS if y_min <= y + dy <= y_max]
    else:
        next_pos = [(x + dx, y, not z) for dx in STEPS if x_min <= x + dx <= x_max]

    return next_pos


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        grid = [line.strip() for line in puzzle.readlines()]

    for i in range(len(grid)):
        grid[i] = [int(tile) for tile in grid[i]]

    return grid


def solver(input_path, puzzle_type):
    # assert puzzle_type in ('energized', 'max')

    grid = loader(input_path)

    # Z vertical? True|False
    tiles = [Head((0, 0, False)), Head((0, 0, True))]
    end = len(grid) - 1, len(grid[0]) - 1

    end_reached = False

    while not end_reached:
        tiles.sort(key=Head.sort_key)

    return min_heat_loss


def run_examples():
    examples = (
        ('test_input', 'heat', 102),
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
    # assert part1 == 
    # assert part2 == 


if __name__ == '__main__':
    run_examples()
    # main()
