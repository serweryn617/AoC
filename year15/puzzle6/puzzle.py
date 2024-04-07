def split_ints(string):
    ints = string.split(',')
    ints = int(ints[0]), int(ints[1])
    return ints


def loader(input_path):
    for line in open(input_path, 'r'):
        elements = line.split()

        if elements[0] == 'turn':
            elements.pop(0)

        op = elements[0]
        start = split_ints(elements[1])
        end = split_ints(elements[3])

        yield op, start, end


def update_grid(grid, start, end, update_func):
    for x in range(start[0], end[0] + 1): # range is inclusive
        for y in range(start[1], end[1] + 1):
            grid[x][y] = update_func(grid[x][y])


def grid_sum(grid):
    total = 0
    for line in grid:
        total += sum(line)
    return total


def solver(input_path, puzzle_type):
    assert puzzle_type in ('part1', 'part2')

    data = loader(input_path)

    if puzzle_type == 'part1':
        op_lut = {
            'on': lambda x: 1,
            'off': lambda x: 0,
            'toggle': lambda x: not x,
        }
    else:
        op_lut = {
            'on': lambda x: x + 1,
            'off': lambda x: max(x - 1, 0),
            'toggle': lambda x: x + 2,
        }

    lights = [[0 for _ in range(1000)] for _ in range(1000)]

    for op, start, end in data:
        update_func = op_lut[op]
        update_grid(lights, start, end, update_func)

    return grid_sum(lights)


def run_examples():
    examples = (
        ('test_input', 'part1', 1000*1000 - 1000 - 4),
        ('test_input', 'part2', 1000*1000*1 + 1000*2 - 4),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'part1')
    part2 = solver('input', 'part2')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 28ms

    # Regression test
    assert part1 == 377891
    assert part2 == 14110788


if __name__ == '__main__':
    run_examples()
    main()
