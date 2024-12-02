def check_sorted(report):
    inc = lambda a, b: a < b <= a + 3
    dec = lambda a, b: a > b >= a - 3

    if inc(report[0], report[1]):
        cmp = inc
    elif dec(report[0], report[1]):
        cmp = dec
    else:
        return False, 0

    for d in range(len(report) - 1):
        if not cmp(report[d], report[d + 1]):
            return False, d

    return True, None


def solve_part1(parsed_input):
    total = 0

    for report in parsed_input:
        if check_sorted(report)[0]:
            total += 1

    return total


def solve_part2(parsed_input):
    total = 0

    for report in parsed_input:
        ok, err = check_sorted(report)
        if ok:
            total += 1
        else:
            # TODO: is there some edge case that would break the inc/dec checking and break here?
            sub_data0 = report[:err - 1] + report[err:]
            ok0, _ = check_sorted(sub_data0)

            sub_data1 = report[:err] + report[err + 1:]
            ok1, _ = check_sorted(sub_data1)

            sub_data2 = report[:err + 1] + report[err + 2:]
            ok2, _ = check_sorted(sub_data2)

            if ok0 or ok1 or ok2:
                total += 1

    return total


def loader(input_path):
    puzzle_input = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            report = list(map(int, line.split()))
            puzzle_input.append(report)

    return puzzle_input


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 2),
        ('test_input', 2, 4),
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
    assert part1 == 670
    assert part2 == 700


if __name__ == '__main__':
    run_examples()
    main()
