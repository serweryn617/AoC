def parse(item):
    num_columns = len(item[0].strip())
    total = [0 for _ in range(num_columns)]

    for c in range(num_columns):
        col = [row[c] for row in item]
        total[c] = col.count('#')

    return total


def check(lock, key):
    pin_sum = map(lambda a, b: a + b, lock, key)

    for s in pin_sum:
        if s >= 8:
            return 0

    return 1


def solve_part1(parsed_input, is_example):
    locks, keys = parsed_input

    keys = [parse(k) for k in keys]
    locks = [parse(l) for l in locks]

    total = 0

    for lock in locks:
        for key in keys:
            total += check(lock, key)

    return total


def solve_part2(parsed_input, is_example):
    return 0


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        data = puzzle.readlines()

    locks = []
    keys = []

    for i in range(0, len(data), 8):
        if data[i][0] == '#':
            locks.append(data[i : i + 7])
        else:
            keys.append(data[i : i + 7])

    return locks, keys


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 3),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type, is_example=True)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 1)

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print(f'Solution found in {took:.3f}s')  # 15ms

    # Regression test
    assert part1 == 3483


if __name__ == '__main__':
    run_examples()
    main()
