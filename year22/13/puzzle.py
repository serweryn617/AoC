from functools import cmp_to_key


def comparator(left, right):
    res = check_order(left, right)
    if res is None:
        return 0
    else:
        return -1 if res else 1


def check_order(left, right):
    def instances(a, b):
        return isinstance(left, a) and isinstance(right, b)

    if instances(int, int):
        if left != right:
            return left < right

    elif instances(int, list):
        res = check_order([left], right)
        if res is not None:
            return res

    elif instances(list, int):
        res = check_order(left, [right])
        if res is not None:
            return res

    elif instances(list, list):
        for n in range(min(len(left), len(right))):
            res = check_order(left[n], right[n])
            if res is not None:
                return res
        if len(left) != len(right):
            return len(left) < len(right)


def solve_part1(parsed_input):
    total = 0
    for n, (left, right) in enumerate(parsed_input):
        c = check_order(left, right)
        if c:
            total += n + 1

    return total


def solve_part2(parsed_input):
    decoder_a = [[2]]
    decoder_b = [[6]]

    packets = [decoder_a, decoder_b]
    for left, right in parsed_input:
        packets += [left, right]

    packets.sort(key=cmp_to_key(comparator))

    return (packets.index(decoder_a) + 1) * (packets.index(decoder_b) + 1)


def loader(input_path):
    left, right = None, None
    parsed_input = []

    with open(input_path, 'r') as puzzle:
        lines = puzzle.readlines()
    
    for l in range(0, len(lines), 3):
        left = lines[l].strip()
        right = lines[l + 1].strip()

        left = eval(left)  # HACK
        right = eval(right)

        parsed_input.append((left, right))

    return parsed_input


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 13),
        ('test_input', 2, 140),
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
    print(f'Solutions found in {took:.3f}s')  # 22ms

    # Regression test
    assert part1 == 5252
    assert part2 == 20592


if __name__ == '__main__':
    run_examples()
    main()
