from functools import cache


OPERATIONAL = '.'
BROKEN = '#'
UNKNOWN = '?'


@cache
def possibilities_recursive(springs, groups, position = 0):
    if not springs:
        return not groups and position == 0

    result = 0
    choices = (OPERATIONAL, BROKEN) if springs[0] == UNKNOWN else springs[0]

    for choice in choices:
        if choice == BROKEN:
            result += possibilities_recursive(springs[1:], groups, position + 1)
        else:  # OPERATIONAL
            if position == 0:
                # '.' without any group, just skip it
                result += possibilities_recursive(springs[1:], groups)
            else:
                if groups and groups[0] == position:
                    result += possibilities_recursive(springs[1:], groups[1:])

    return result


def simplify_springs(springs):
    for i in range(len(springs)):
        springs[i] = '.'.join(springs[i].replace('.', ' ').split())


def add_to_cache(args, result):
    ...


def loader(input_path):
    springs = []
    groups = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            springs_row, groups_row = line.split()

            groups_row = tuple(map(int, groups_row.split(',')))

            springs.append(springs_row)
            groups.append(groups_row)

    return springs, groups


def solver(input_path, puzzle_type):
    springs, groups = loader(input_path)

    if puzzle_type == 'unfold':
        for i in range(len(springs)):
            springs[i] = '?'.join([springs[i]] * 5)
            groups[i] = groups[i] * 5

    simplify_springs(springs)
    total = 0

    for s, g in zip(springs, groups):
        a = possibilities_recursive(s + '.', g)
        total += a

    return total


def run_examples():
    examples = (
        ('test_input', 'possible', 21),
        ('test_input', 'unfold', 525152),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'possible')
    part2 = solver('input', 'unfold')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 1600ms

    # Regression test
    assert part1 == 7792
    assert part2 == 13012052341533


if __name__ == '__main__':
    run_examples()
    main()
