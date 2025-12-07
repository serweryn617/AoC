ROLL = "@"
POSITIONS = (
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1),
)


def count_around(grid, x, y, char=ROLL):
    count = 0
    for dx, dy in POSITIONS:
        check_x = x + dx
        check_y = y + dy

        if check_y < 0 or check_y >= len(grid) or check_x < 0 or check_x >= len(grid[y]):
            continue

        if grid[check_y][check_x] == char:
            count += 1
    return count


def solve_part1(parsed_input):
    total = 0
    for y in range(len(parsed_input)):
        for x in range(len(parsed_input[0])):
            if parsed_input[y][x] != ROLL:
                continue

            count = count_around(parsed_input, x, y)
            if count < 4:
                total += 1
    return total


def remove_rolls(grid, to_remove):
    total = 0
    while to_remove:
        rem_x, rem_y = to_remove.pop(0)

        if grid[rem_y][rem_x] != ROLL:
            continue

        count = count_around(grid, rem_x, rem_y)
        if not (count < 4):
            continue

        total += 1
        grid[rem_y] = grid[rem_y][:rem_x] + 'x' + grid[rem_y][rem_x + 1:]

        for dx, dy in POSITIONS:
            check_x = rem_x + dx
            check_y = rem_y + dy

            if check_y < 0 or check_y >= len(grid) or check_x < 0 or check_x >= len(grid[rem_y]):
                continue

            if grid[check_y][check_x] == ROLL:
                to_remove.append((check_x, check_y))

    return total


def solve_part2(parsed_input):
    to_remove = []
    for y in range(len(parsed_input)):
        for x in range(len(parsed_input[0])):
            if parsed_input[y][x] != ROLL:
                continue

            count = count_around(parsed_input, x, y)
            if count < 4:
                to_remove.append((x, y))

    total = remove_rolls(parsed_input, to_remove)

    return total


def loader(input_path):
    data = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle:
            data.append(line.strip())

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
        ('test_input', 1, 13),
        ('test_input', 2, 43),
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
    print(f'Solutions found in {took:.3f}s')  # 2ms

    # Regression test
    assert part1 == 1449
    assert part2 == 8746


if __name__ == '__main__':
    run_examples()
    main()
