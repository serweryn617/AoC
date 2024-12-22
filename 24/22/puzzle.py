def mix_prune(mix, x):
    secret = mix ^ x
    secret = secret % 16777216
    return secret


def randomize(x):
    mix = x * 64
    x = mix_prune(mix, x)
    mix = x // 32
    x = mix_prune(mix, x)
    mix = x * 2048

    return mix_prune(mix, x)


def fast_randomize(x):
    x = (x << 6 ^ x) & 0xffffff
    x = (x >> 5 ^ x) & 0xffffff
    return (x << 11 ^ x) & 0xffffff


def solve_part1(numbers, is_example):
    total = 0

    for n in numbers:
        for _ in range(2000):
            n = fast_randomize(n)
        total += n

    return total


def digit_diff(a, b):
    return a % 10 - b % 10


def diff_sequence(n, i):
    prices = []
    diffs = []
    prev = n

    for _ in range(i - 1):
        n = fast_randomize(n)
        diffs.append(digit_diff(n, prev))
        prices.append(n % 10)
        prev = n

    return prices, diffs


def solve_part2(numbers, is_example):
    sequences = {}

    for n in numbers:
        prices, diffs = diff_sequence(n, 2000)
        added = set()
        for i in range(len(diffs) - 4):
            key = tuple(diffs[i : i + 4])
            val = prices[i + 3]

            if key in added:
                continue

            added.add(key)
            if key not in sequences:
                sequences[key] = val
            else:
                sequences[key] += val

    _, res = max(sequences.items(), key=lambda i: i[1])
    return res


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        numbers = [int(l.strip()) for l in puzzle.readlines()]

    return numbers


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 37327623),
        ('test_input2', 2, 23),
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
    print(f'Solutions found in {took:.3f}s')  # 3277ms

    # Regression test
    assert part1 == 20068964552
    assert part2 == 2246


if __name__ == '__main__':
    run_examples()
    main()
