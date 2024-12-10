DIRECTIONS = (1, 0), (-1, 0), (0, 1), (0, -1), 


def reachable_peaks(grid, pos, trail):
    x, y = pos
    if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
        return ()
    if grid[y][x] != trail[0]:
        return ()
    if grid[y][x] == trail[0] and len(trail) == 1:
        return ((x, y),)

    reachable = []
    for dx, dy in DIRECTIONS:
        next_pos = x + dx, y + dy
        add = reachable_peaks(grid, next_pos, trail[1:])
        add = filter(lambda p: bool(p), add)
        reachable.extend(add)
    return reachable


def solve_part1(grid):
    total = 0
    trail = list(range(10))
    
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            reachable = reachable_peaks(grid, (x, y), trail)
            total += len(set(reachable))

    return total


def solve_part2(grid):
    total = 0
    trail = list(range(10))
    
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            reachable = reachable_peaks(grid, (x, y), trail)
            total += len(reachable)

    return total


def loader(input_path):
    grid = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            grid.append([int(i) for i in line.strip()])

    return grid


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 36),
        ('test_input', 2, 81),
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
    print(f'Solutions found in {took:.3f}s')  # 13ms

    # Regression test
    assert part1 == 548
    assert part2 == 1252


if __name__ == '__main__':
    run_examples()
    main()
