def get_joltage(bank):
    first = max(bank[:-1])
    first_index = bank.find(first)

    second = max(bank[first_index + 1:])

    return int(first + second)


def solve_part1(parsed_input):
    total = 0
    for bank in parsed_input:
        total += get_joltage(bank)
    return total


def get_joltage_n(bank, n=12):
    digits = [0 for i in range(n)]

    for i in range(n):
        reserved = n - i - 1
        if reserved != 0:
            available = bank[:-reserved]
        else:
            available = bank
        digit = max(available)
        index = bank.find(digit)
        bank = bank[index + 1:]
        digits[i] = digit

    return int("".join(digits))


def solve_part2(parsed_input):
    total = 0
    for bank in parsed_input:
        total += get_joltage_n(bank)
    return total


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
        ('test_input', 1, 357),
        ('test_input', 2, 3121910778619),
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
    print(f'Solutions found in {took:.3f}s')  # 2ms

    # Regression test
    assert part1 == 17445
    assert part2 == 173229689350551


if __name__ == '__main__':
    run_examples()
    main()
