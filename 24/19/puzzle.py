from functools import cache


def possible(combination, towels):
    if not combination:
        return True

    max_towel_len = max(map(len, towels))

    for i in range(1, max_towel_len + 1):
        start = combination[:i]
        if start not in towels:
            continue

        end = combination[i:]
        ok = possible(end, towels)
        if ok:
            return True

    return False


@cache
def num_ways(combination, towels):
    if not combination:
        return 1

    count = 0
    max_towel_len = max(map(len, towels))
    max_check_len = min(max_towel_len, len(combination))

    for i in range(1, max_check_len + 1):
        start = combination[:i]
        if start not in towels:
            continue

        end = combination[i:]
        count += num_ways(end, towels)

    return count


def solve_part1(parsed_input, is_example):
    towels, combinations = parsed_input

    count = 0
    for combination in combinations:
        ok = possible(combination, towels)
        if ok:
            count += 1

    return count


def solve_part2(parsed_input, is_example):
    towels, combinations = parsed_input

    count = 0
    for n, combination in enumerate(combinations):
        p = num_ways(combination, tuple(towels))
        count += p

    return count


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        towels = puzzle.readline().strip().split(', ')
        puzzle.readline()
        combinations = [l.strip() for l in puzzle.readlines()]

    return towels, combinations


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 6),
        ('test_input', 2, 16),
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
    print(f'Solutions found in {took:.3f}s')  # 363ms

    # Regression test
    assert part1 == 233
    assert part2 == 691316989225259


if __name__ == '__main__':
    run_examples()
    main()
