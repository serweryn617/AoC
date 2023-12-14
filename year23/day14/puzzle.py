SOLID = '#'
ROUND = 'O'
EMPTY = '.'


def rotate_right(pattern):
    rotated = []

    for i in range(len(pattern[0])):
        new_line = ''
        for row in pattern:
            new_line = row[i] + new_line
        rotated.append(new_line)

    return rotated


def linear_sequence_sum(start, count):
    return (2 * start - count + 1) * count // 2


def roll_row(row):
    ranges = row.split(SOLID)
    rolled_ranges = []

    for r in ranges:
        num_stones = r.count(ROUND)
        num_empty = len(r) - num_stones
        rolled_ranges.append(ROUND * num_stones + EMPTY * num_empty)

    return SOLID.join(rolled_ranges)


def roll_stones(pattern):
    rolled_pattern = []

    for row in pattern:
        rolled_pattern.append(roll_row(row))

    return rolled_pattern


def get_row_load(row, max_load):
    total_load = 0

    for stone, val in zip(row, range(max_load, 0, -1)):
        if stone == ROUND:
            total_load += val

    return total_load


def get_load(pattern, max_load):
    total = 0

    for row in pattern:
        total += get_row_load(row, max_load)

    return total


def loader(input_path):
    pattern = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            pattern.append(line.rstrip())

    return pattern


def solver(input_path, num_cycles):
    # Is there a better approach possible?

    pattern = loader(input_path)

    max_load = len(pattern)

    # Everything is calculated from the left
    # rotate the input, so north is on the left
    pattern = rotate_right(pattern)
    pattern = rotate_right(pattern)
    pattern = rotate_right(pattern)

    uniques = {}
    pattern_cycles = None

    for n in range(num_cycles):
        for _ in range(4):
            pattern = roll_stones(pattern)
            pattern = rotate_right(pattern)

        key = ''.join(pattern)
        if key in uniques:
            pattern_cycles = True
            break
        else:
            uniques[key] = n

    if pattern_cycles:
        cycle = n - uniques[key]
        additional = (num_cycles - uniques[key] - 1) % cycle  # subtract 1 - first unique is 0

        for _ in range(additional):
            for _ in range(4):
                pattern = roll_stones(pattern)
                pattern = rotate_right(pattern)

    if num_cycles == 0:
        pattern = roll_stones(pattern)

    return get_load(pattern, max_load)


def run_examples():
    examples = (
        ('test_input', 0, 136),
        ('test_input', 1, 87),
        ('test_input', 2, 69),
        ('test_input', 3, 69),
        ('test_input', 1000000000, 64),
    )

    for path, num_cycles, expected in examples:
        result = solver(path, num_cycles)
        assert result == expected, f'Example {path} {num_cycles} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 0)
    part2 = solver('input', 1000000000)

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 229ms

    # Regression test
    assert part1 == 109424
    assert part2 == 102509


if __name__ == '__main__':
    run_examples()
    main()
