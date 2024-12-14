def solve_part1(parsed_input, is_example):
    return 0


def solve_part2(parsed_input, is_example):
    return 0


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            pass

    return None


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 0),
        ('test_input', 2, 0),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type, is_example=True)
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
    print(f'Solutions found in {took:.3f}s')  # 0ms

    # Regression test
    # assert part1 == 0
    # assert part2 == 0


if __name__ == '__main__':
    run_examples()
    # main()
