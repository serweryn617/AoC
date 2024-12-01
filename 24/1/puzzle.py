def solve_part1(parsed_input):
    list_a, list_b = parsed_input
    list_a.sort()
    list_b.sort()
    distances = [abs(a - b) for a, b in zip(list_a, list_b)]
    return sum(distances)


def solve_part2(parsed_input):
    list_a, list_b = parsed_input
    result = 0

    for a in list_a:
        count = list_b.count(a)
        result += a * count

    return result


def loader(input_path):
    list_a, list_b = [], []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            a, b = line.split()
            list_a.append(int(a))
            list_b.append(int(b))

    return list_a, list_b


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 11),
        ('test_input', 2, 31),
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
    print(f'Solutions found in {took:.3f}s')  # 6ms

    # Regression test
    # assert part1 == 3714264
    # assert part2 == 18805872


if __name__ == '__main__':
    run_examples()
    main()
