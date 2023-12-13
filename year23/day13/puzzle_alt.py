# Alternative approach to part 1 of the puzzle which is ~5.7X faster than solution in puzzle.py


def transpose(pattern):
    transposed = []

    for i in range(len(pattern[0])):
        new_line = ''
        for p in pattern:
            new_line = new_line + p[i]
        transposed.append(new_line)

    return transposed


def find_possible_mirrors(pattern):
    possible = []

    for i in range(1, len(pattern)):
        if pattern[i - 1] == pattern[i]:
            possible.append(i)

    return possible


def validate_horizontal_mirror(pattern, idx_mirror):
    # mirror between indexes idx_mirror and idx_mirror - 1

    plen = len(pattern)

    num_mirrored = min(idx_mirror, plen - idx_mirror)

    original = pattern[idx_mirror - num_mirrored:idx_mirror]
    reflection = pattern[idx_mirror:idx_mirror + num_mirrored]
    reflection.reverse()

    if original == reflection:
        return idx_mirror


def get_mirror(pattern):
    possible = find_possible_mirrors(pattern)
    if possible:
        for pos in possible:
            mirror = validate_horizontal_mirror(pattern, pos)
            if mirror is not None:
                return mirror


def loader(input_path):
    patterns = [[]]

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            line = line.rstrip()
            if not line:
                patterns.append([])
            else:
                patterns[-1].append(line)

    return patterns


def solver(input_path):
    patterns = loader(input_path)

    total = 0

    for pattern in patterns:
        mirror = None
        multiplier = 100
        mirror = get_mirror(pattern)

        if mirror is None:
            multiplier = 1
            pattern = transpose(pattern)
            mirror = get_mirror(pattern)

        total += mirror * multiplier

    return total


def run_examples():
    examples = (
        ('test_input', 405),
    )

    for path, expected in examples:
        result = solver(path)
        assert result == expected, f'Example {path} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print(f'Both solutions found in {took:.3f}s')  # <1ms

    # Regression test
    assert part1 == 33195


if __name__ == '__main__':
    run_examples()
    main()
