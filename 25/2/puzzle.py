def get_halves(num):
    string = str(num)
    length = len(string) // 2
    up = string[:length]
    dn = string[length:]
    return int(up), int(dn)


def calc_invalid_ids(a, b):
    min_num_digits = (len(str(a)) + 1) // 2
    max_num_digits = (len(str(b))) // 2

    a = max(a, 10 ** (min_num_digits * 2 - 1))
    b = min(b, (10 ** (max_num_digits * 2)) - 1)

    odd_num_of_digits_range = a > b
    if odd_num_of_digits_range:
        return 0

    assert len(str(a)) % 2 == 0
    assert len(str(b)) % 2 == 0
    assert len(str(a)) == len(str(b))

    up_a, dn_a = get_halves(a)
    up_b, dn_b = get_halves(b)

    start = up_a if up_a >= dn_a else up_a + 1
    end = up_b if up_b <= dn_b else up_b - 1

    if start > end:
        return 0

    length = end - start + 1
    total = int(length * (start + end) / 2)

    num_digits = len(str(up_a))
    total *= (10 ** num_digits + 1)

    return total


def solve_part1(parsed_input):
    total = 0
    for a, b in parsed_input:
        total += calc_invalid_ids(a, b)
    return total


def solve_part2(parsed_input):
    pass


def loader(input_path):
    data = []

    with open(input_path, 'r') as puzzle:
        raw_data = puzzle.read()

    ranges = raw_data.strip().split(",")
    for entry in ranges:
        a, b = entry.split("-")
        d = sorted((int(a), int(b)))
        data.append(tuple(d))

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
        ('test_input', 1, 1227775554),
        # ('test_input', 2, 4174379265),
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
    print(f'Solutions found in {took:.3f}s')  # <1ms

    # Regression test
    assert part1 == 24043483400
    # assert part2 == 6122


if __name__ == '__main__':
    run_examples()
    main()
