
def manhattan_distance(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return dx + dy


def sum_distances(stars):
    distance = 0

    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            distance += manhattan_distance(stars[i], stars[j])
    
    return distance


def expand(stars, expansion):
    el = set(s[0] for s in stars)
    az = set(s[1] for s in stars)
    el_range = set(range(max(el) + 1))
    az_range = set(range(max(az) + 1))

    empty_el = el_range - el
    empty_az = az_range - az

    for n in range(len(stars)):
        e, a = stars[n]
        expand_el_by = len([i for i in empty_el if i < e])
        expand_az_by = len([i for i in empty_az if i < a])

        stars[n][0] += expand_el_by * expansion
        stars[n][1] += expand_az_by * expansion

    return stars


def loader(input_path):
    stars = []

    with open(input_path, 'r') as puzzle:
        for elevation, line in enumerate(puzzle.readlines()):
            for azymuth, space in enumerate(line):
                if space == '#':
                    stars.append([elevation, azymuth])

    return stars


def solver(input_path, expansion):
    stars = loader(input_path)
    stars = expand(stars, expansion)
    puzzle_answer = sum_distances(stars)

    return puzzle_answer


def run_examples():
    examples = (
        ('test_input', 1, 374),
        ('test_input', 9, 1030),
        ('test_input', 99, 8410),
    )

    for path, expansion, expected in examples:
        result = solver(path, expansion)
        assert result == expected, f'Example {path} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 1)
    part2 = solver('input', 999999)  # replace 1 empty row with 1M rows, or expand by 999999

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 17ms

    # Regression test
    assert part1 == 9693756
    assert part2 == 717878258016


if __name__ == '__main__':
    run_examples()
    main()
