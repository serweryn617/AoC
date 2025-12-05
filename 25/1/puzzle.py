START = 50


def solve_part1(parsed_input):
    total = 0
    pos = START
    for d, v in parsed_input:
        if d == "L":
            pos -= v
        if d == "R":
            pos += v
        pos %= 100
        if pos == 0:
            total += 1
    return total


def solve_part2(parsed_input):
    total = 0
    pos = START
    for d, v in parsed_input:
        if d == "L":
            start = (100 - pos) // 100
            end = (100 - pos + v) // 100
            total += end - start
            pos -= v

        if d == "R":
            end = (pos + v) // 100
            total += end
            pos += v

        pos %= 100
    return total


def loader(input_path):
    data = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            d = line[0]
            v = int(line[1:])
            data.append((d, v))

    return data


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 3),
        ('test_input', 2, 6),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 1)
    part2 = solver('input', 2)

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Solutions found in {took:.3f}s')  # 3ms

    # Regression test
    assert part1 == 1064
    assert part2 == 6122


if __name__ == '__main__':
    run_examples()
    main()
