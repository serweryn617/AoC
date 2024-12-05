from functools import cmp_to_key


def check_rule(manual, rule):
    if rule[0] not in manual or rule[1] not in manual:
        return True

    a = manual.index(rule[0])
    b = manual.index(rule[1])
    return a < b


def is_sorted(manual, rules):
    for rule in rules:
        ok = check_rule(manual, rule)

        if not ok:
            return False

    return True


def solve_part1(parsed_input):
    rules, manuals = parsed_input
    total = 0

    for manual in manuals:
        ok = is_sorted(manual, rules)
        if ok:
            mid_idx = (len(manual) - 1) // 2
            total += manual[mid_idx]

    return total


def solve_part2(parsed_input):
    rules, manuals = parsed_input
    total = 0

    def comparator(a, b):
        if (a, b) in rules:
            return 1
        if (b, a) in rules:
            return -1
        return 0

    for manual in manuals:
        ok = is_sorted(manual, rules)
        if not ok:
            n = sorted(manual, key=cmp_to_key(comparator))
            mid_idx = (len(n) - 1) // 2
            total += n[mid_idx]

    return total


def loader(input_path):
    rules = []
    manuals = []

    is_rule = True

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            if line == '\n':
                is_rule = False
                continue

            if is_rule:
                rule = line.split('|')
                rules.append(tuple(int(r) for r in rule))
            else:
                manual = line.split(',')
                manuals.append(tuple(int(m) for m in manual))

    return rules, manuals


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 143),
        ('test_input', 2, 123),
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
    print(f'Solutions found in {took:.3f}s')  # 72ms

    # Regression test
    assert part1 == 4957
    assert part2 == 6938


if __name__ == '__main__':
    run_examples()
    main()
