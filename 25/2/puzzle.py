def get_halves(num):
    string = str(num)
    length = len(string) // 2
    up = string[:length]
    dn = string[length:]
    return int(up), int(dn)


# NOTE: could use part 2 solution for part one as well
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


def matching_ranges(ranges):
    matching = []
    for a, b in ranges:
        len_a, len_b = len(str(a)), len(str(b))

        if len_a == len_b:
            matching.append((a, b))
            continue

        assert abs(len_a - len_b) == 1

        a_upper = 10 ** len_a - 1
        b_lower = 10 ** (len_b - 1)

        matching.append((a, a_upper))
        matching.append((b_lower, b))

    return matching


def digits_1(a, b):
    len_a, len_b = len(str(a)), len(str(b))
    assert len_a == len_b

    total = 0
    base = int('1' * len_a)
    for i in range(base, base * 10, base):
        if a <= i <= b:
            total += i

    return total


def start_groups_valid(groups):
    start, *rest = groups
    for r in rest:
        if start < r:
            return False
        if start > r:
            return True
    return True


def end_groups_valid(groups):
    end, *rest = groups
    for r in rest:
        if end < r:
            return True
        if end > r:
            return False
    return True


def digits_above_1(a, b, n=2):
    str_a, str_b = str(a), str(b)
    len_a, len_b = len(str_a), len(str_b)
    assert len_a == len_b

    start_groups = [int(str_a[i:i+n]) for i in range(0, len_a, n)]
    end_groups = [int(str_b[i:i+n]) for i in range(0, len_b, n)]

    start = start_groups[0]
    if not start_groups_valid(start_groups):
        assert len(str(start)) == len(str(start + 1))
        start += 1

    end = end_groups[0]
    if not end_groups_valid(end_groups):
        assert end > 0
        end -= 1

    if start > end:
        return 0

    count = end - start + 1
    assert (count * (start + end)) % 2 == 0
    total = int(count * (start + end) / 2)

    val_mod = int(('1' + '0' * (n - 1)) * (len(start_groups) - 1) + '1')
    total = total * val_mod

    return total


def digits(a, b, n):
    if n == 1:
        return digits_1(a, b)
    return digits_above_1(a, b, n)


LUT = {
    1: lambda a, b: 0,
    2: lambda a, b: digits(a, b, 1),
    3: lambda a, b: digits(a, b, 1),
    4: lambda a, b: digits(a, b, 2),
    5: lambda a, b: digits(a, b, 1),
    6: lambda a, b: digits(a, b, 3) + digits(a, b, 2) - digits(a, b, 1),
    7: lambda a, b: digits(a, b, 1),
    8: lambda a, b: digits(a, b, 4),
    9: lambda a, b: digits(a, b, 3),
    10: lambda a, b: digits(a, b, 5) + digits(a, b, 2) - digits(a, b, 1),
}


def solve_part2(parsed_input):
    matching = matching_ranges(parsed_input)
    total = 0
    for a, b in matching:
        num_digits = len(str(a))
        total += LUT[num_digits](a, b)
    return total


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
        ('test_input', 2, 4174379265),
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
    print(f'Solutions found in {took:.3f}s')  # <1ms

    # Regression test
    assert part1 == 24043483400
    assert part2 == 38262920235


if __name__ == '__main__':
    run_examples()
    main()
