from math import prod


OPS = {
    '+': sum,
    '*': prod,
}


def solve_part1(parsed_input):
    *vals, ops = parsed_input

    vals = [[int(v) for v in val.split()] for val in vals]
    ops = ops.split()

    total = 0

    for *v, op in zip(*vals, ops):
        total += OPS[op](v)

    return total


def solve_part2(parsed_input):
    *vals, ops = parsed_input

    longest_line = max((len(v) for v in vals))
    vals = [v.ljust(longest_line) for v in vals]

    new_vals = [[]]
    for v in zip(*vals, strict=True):
        if all((c == ' ' for c in v)):
            new_vals.append([])
        else:
            number = int(''.join(v))
            new_vals[-1].append(number)

    ops = ops.split()
    assert len(new_vals) == len(ops)

    total = 0
    for v, op in zip(new_vals, ops):
        total += OPS[op](v)
    return total


def loader(input_path):
    data = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            data.append(line.rstrip())

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
        ('test_input', 1, 4277556),
        ('test_input', 2, 3263827),
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
    assert part1 == 4693159084994
    assert part2 == 11643736116335


if __name__ == '__main__':
    run_examples()
    main()
