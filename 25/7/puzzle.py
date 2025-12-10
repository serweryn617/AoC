from functools import cache

START = "S"
SPLIT = "^"


def beam_recursive(grid, x, y, visited):
    if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
        return 0

    if (x, y) in visited:
        return 0
    visited.add((x, y))

    num_splits = 0

    if grid[y][x] == SPLIT:
        num_splits += 1
        num_splits += beam_recursive(grid, x + 1, y, visited)
        num_splits += beam_recursive(grid, x - 1, y, visited)
    else:
        num_splits += beam_recursive(grid, x, y + 1, visited)

    return num_splits


def solve_part1(grid):
    x, y = grid[0].find(START), 0

    visited = set()
    res = beam_recursive(grid, x, y, visited)

    return res


@cache
def cached_beam_all_recursive(grid, x, y):
    if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
        return 0

    num_splits = 0

    if grid[y][x] == SPLIT:
        num_splits += 1
        num_splits += cached_beam_all_recursive(grid, x + 1, y)
        num_splits += cached_beam_all_recursive(grid, x - 1, y)
    else:
        num_splits += cached_beam_all_recursive(grid, x, y + 1)

    return num_splits


def solve_part2(grid):
    x, y = grid[0].find(START), 0

    res = cached_beam_all_recursive(tuple(grid), x, y)

    return res + 1


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
        ('test_input', 1, 21),
        ('test_input', 2, 40),
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
    print(f'Solutions found in {took:.3f}s')  # 10ms

    # Regression test
    assert part1 == 1675
    assert part2 == 187987920774390


if __name__ == '__main__':
    run_examples()
    main()
