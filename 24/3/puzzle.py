import re


def solve_part1(parsed_input):
    total = 0
    matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', parsed_input)

    for a, b in matches:
        total += int(a) * int(b)
    
    return total


def solve_part2(parsed_input):
    total = 0
    enabled = re.findall(r"(?:^|do\(\))(.*?)(?:$|don't\(\))", parsed_input)

    for e in enabled:
        total += solve_part1(e)
    
    return total


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        lines = puzzle.readlines()

    return ''.join((l.strip() for l in lines))


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 161),
        ('test_input_2', 2, 48),
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
    print(f'Solutions found in {took:.3f}s')  # 1ms

    # Regression test
    assert part1 == 179834255
    assert part2 == 80570939


if __name__ == '__main__':
    run_examples()
    main()
