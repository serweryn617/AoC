def solve_part1(parsed_input):
    return 0


def solve_part2(parsed_input):
    return 0


def loader(input_path):
    data = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle:
            data.append(line.strip())

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
        ('test_input', 1, 0),
        # ('test_input', 2, 0),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 1)
    # part2 = solver('input', 2)

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    # print('Puzzle 2 answer:', part2)
    print(f'Solutions found in {took:.3f}s')  # xms

    # Regression test
    # assert part1 == 0
    # assert part2 == 0


if __name__ == '__main__':
    run_examples()
    # main()
