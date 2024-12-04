def search(grid, word, point, direction):
    if not word:
        return True

    x, y = point
    len_x = len(grid[0])
    len_y = len(grid)

    if 0 > x or x >= len_x or 0 > y or y >= len_y:
        return False

    if grid[y][x] != word[0]:
        return False

    nx, ny = point[0] + direction[0], point[1] + direction[1]
    return search(grid, word[1:], (nx, ny), direction)


def solve_part1(parsed_input):
    word = 'XMAS'
    count = 0

    AROUND = (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)

    for y, row in enumerate(parsed_input):
        for x, point in enumerate(row):
            for d in AROUND:
                r = search(parsed_input, word, (x, y), d)
                if r: 
                    count += 1

    return count


def solve_part2(grid):
    count = 0

    len_x = len(grid[0])
    len_y = len(grid)

    for x in range(1, len_x - 1):
        for y in range(1, len_y - 1):
            if grid[y][x] != 'A':
                continue

            diag_a_ok = False
            crd_a = grid[y - 1][x - 1]
            crd_b = grid[y + 1][x + 1]
            if (crd_a == 'M' and crd_b == 'S') or (crd_a == 'S' and crd_b == 'M'):
                diag_a_ok = True

            diag_b_ok = False
            crd_c = grid[y + 1][x - 1]
            crd_d = grid[y - 1][x + 1]
            if (crd_c == 'M' and crd_d == 'S') or (crd_c == 'S' and crd_d == 'M'):
                diag_b_ok = True

            if diag_a_ok and diag_b_ok:
                count += 1

    return count


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        lines = [l.strip() for l in puzzle.readlines()]

    return lines


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 18),
        ('test_input', 2, 9),
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
    print(f'Solutions found in {took:.3f}s')  # 30ms

    # Regression test
    assert part1 == 2536
    assert part2 == 1875


if __name__ == '__main__':
    run_examples()
    main()
