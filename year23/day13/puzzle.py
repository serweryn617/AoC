def transpose(pattern):
    transposed = []

    for i in range(len(pattern[0])):
        new_line = ''
        for p in pattern:
            new_line = new_line + p[i]
        transposed.append(new_line)

    return transposed


def all_possible_mirrors(pattern):
    possible = []
    plen = len(pattern)

    for idx_mirror in range(1, plen):
        num_mirrored = min(idx_mirror, plen - idx_mirror)

        original = pattern[idx_mirror - num_mirrored:idx_mirror]
        reflection = pattern[idx_mirror:idx_mirror + num_mirrored]
        reflection.reverse()

        possible.append((original, reflection))

    return possible


def validate_horizontal_mirror(original, reflection):
    num_smudges = 0
    
    for org, ref in zip(original, reflection):
        for a, b in zip(org, ref):
            if a != b:
                num_smudges += 1

    return num_smudges


def get_mirror_location(pattern, num_smudges):
    possible = all_possible_mirrors(pattern)

    for n, pos in enumerate(possible):
        if validate_horizontal_mirror(pos[0], pos[1]) == num_smudges:
            return n + 1


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


def solver(input_path, num_smudges):
    patterns = loader(input_path)

    total = 0

    for pattern in patterns:
        mirror = None
        multiplier = 100
        mirror = get_mirror_location(pattern, num_smudges)

        if mirror is None:
            multiplier = 1
            pattern = transpose(pattern)
            mirror = get_mirror_location(pattern, num_smudges)

        total += mirror * multiplier

    return total


def run_examples():
    examples = (
        ('test_input', 0, 405),
        ('test_input', 1, 400),
    )

    for path, num_smudges, expected in examples:
        result = solver(path, num_smudges)
        assert result == expected, f'Example {path} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 0)
    part2 = solver('input', 1)

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 5ms

    # Regression test
    assert part1 == 33195
    assert part2 == 31836


if __name__ == '__main__':
    run_examples()
    main()
