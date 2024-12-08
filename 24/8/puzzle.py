def get_antinodes(a, b, dim, max_num=1):
    dx, dy = a[0] - b[0], a[1] - b[1]
    antinodes = []

    for i in range(1, max_num + 1):
        anti_a = a[0] + dx * i, a[1] + dy * i
        if 0 <= anti_a[0] < dim[0] and 0 <= anti_a[1] < dim[1]:
            antinodes.append(anti_a)
        else:
            break

    for i in range(1, max_num + 1):
        anti_b = b[0] - dx * i, b[1] - dy * i
        if 0 <= anti_b[0] < dim[0] and 0 <= anti_b[1] < dim[1]:
            antinodes.append(anti_b)
        else:
            break

    return antinodes


def print_result(dim, antennas, antinodes):
    positions = {}
    for key, values in antennas.items():
        for pos in values:
            positions[pos] = key

    print("Map:")
    for y in range(dim[1]):
        for x in range(dim[0]):
            if (x, y) in positions:
                c = positions[(x, y)]
                print(c, end='')
            elif (x, y) in antinodes:
                print('#', end='')
            else:
                print('.', end='')
        print()


def solve_part1(parsed_input):
    antennas, dim = parsed_input
    antinodes = set()
    
    for freq, positions in antennas.items():
        count = len(positions)
        for a in range(count - 1):
            for b in range(a + 1, count):
                antinodes.update(get_antinodes(positions[a], positions[b], dim))

    return len(antinodes)


def solve_part2(parsed_input):
    antennas, dim = parsed_input
    antinodes = set()
    max_num = max(dim)
    
    for freq, positions in antennas.items():
        count = len(positions)
        for a in range(count - 1):
            for b in range(a + 1, count):
                anti = get_antinodes(positions[a], positions[b], dim, max_num)
                antinodes.update(anti)
                antinodes.update((positions[a], positions[b]))

    # print_result(dim, antennas, antinodes)

    return len(antinodes)


def loader(input_path):
    antennas = {}

    with open(input_path, 'r') as puzzle:
        for y, line in enumerate(puzzle.readlines()):
            for x, c in enumerate(line.strip()):
                if c == '.':
                    continue

                if c not in antennas:
                    antennas[c] = [(x, y)]
                else:
                    antennas[c].append((x, y))

    return antennas, (x + 1, y + 1)


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 14),
        ('test_input', 2, 34),
        ('test_input2', 2, 9),
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
    print(f'Solutions found in {took:.3f}s')  # 1ms

    # Regression test
    assert part1 == 299
    assert part2 == 1032


if __name__ == '__main__':
    run_examples()
    main()
