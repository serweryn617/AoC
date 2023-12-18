OPERATIONAL = '.'
BROKEN = '#'
UNKNOWN = '?'


def permutations(spaces, total):
    inc = [spaces ** i for i in range(total)]
    pos = [0] * total

    for i in range(spaces ** total):
        a = [1] * spaces
        a[0] = 0
        a[-1] = 0

        for j in pos:
            a[j] += 1

        yield tuple(a)

        for n, j in enumerate(inc):
            if i % j == 0:
                pos[n] += 1
                pos[n] %= spaces


def get_springs_line(group, perm):
    line = []

    for i in range(len(group) + len(perm)):
        if i % 2 == 0:  # perm
            idx = i // 2
            ran = perm[idx]
            c = '.'
        else:
            idx = (i - 1) // 2
            ran = group[idx]
            c = '#'

        for _ in range(ran):
            line.append(c)

    return ''.join(line)


def validate_springs(test, allowed):
    for t, a in zip(test, allowed):
        if (t == '.' and a == '#') or (t == '#' and a == '.'):
            return False
    return True


def loader(input_path):
    springs = []
    groups = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            springs_row, groups_row = line.split()

            springs_row = '.'.join(springs_row.replace('.', ' ').split())
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

    total = 0

    for s, g in zip(springs, groups):
        spaces = len(g) + 1
        num_extra_spaces = len(s) - (sum(g) + len(g) - 1)

        for perm in permutations(spaces, num_extra_spaces):
            line = get_springs_line(g, perm)
            total += validate_springs(line, s)

            # print(line, g, valid)

    return total


def run_examples():
    examples = (
        ('test_input', 'possible', 21),
        # ('test_input', 'unfold', 525152),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'possible')
    # part2 = solver('input', 'unfold')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    # print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 39000ms

    # Regression test
    assert part1 == 7792
    # assert part2 == 


if __name__ == '__main__':
    run_examples()
    main()
