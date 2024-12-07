def concat(a, b):
    return int(f"{a}{b}")


def evaluate(current, target, components, use_concat=False):
    if not components:
        return current == target
    elif current > target:
        return False

    comp, *new_comp = components

    if use_concat:
        current0 = concat(current, comp)
        res0 = evaluate(current0, target, new_comp, use_concat)
        if res0:
            return True

    current1 = current + comp
    res1 = evaluate(current1, target, new_comp, use_concat)
    if res1:
        return True

    current2 = current * comp
    res2 = evaluate(current2, target, new_comp, use_concat)
    return res2


def solve_part1(parsed_input):
    total = 0
    
    for target, first, *components in parsed_input:
        if evaluate(first, target, components):
            total += target

    return total


def solve_part2(parsed_input):
    total = 0
    
    for target, first, *components in parsed_input:
        if evaluate(first, target, components, use_concat=True):
            total += target

    return total


def loader(input_path):
    data = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            components = line.split()
            components[0] = components[0][:-1]
            components = list(map(int, components))
            data.append(components)

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
        ('test_input', 1, 3749),
        ('test_input', 2, 11387),
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
    print(f'Solutions found in {took:.3f}s')  # 1210ms

    # Regression test
    assert part1 == 21572148763543
    assert part2 == 581941094529163


if __name__ == '__main__':
    run_examples()
    main()
