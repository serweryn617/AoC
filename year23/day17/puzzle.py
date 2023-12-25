def step(head, grid, limits):
    heat, x, y, step_vertical = head

    x_min, x_max = 0, len(grid[0]) - 1
    y_min, y_max = 0, len(grid) - 1

    next_heads = []

    # TODO: cleanup
    if step_vertical:
        for delta in range(-limits[1], limits[1] + 1):
            if abs(delta) < limits[0] or not y_min <= y + delta <= y_max:
                continue

            visited = [(x, vy) for vy in range(min(y, y + delta), max(y, y + delta) + 1)]
            visited.pop(visited.index((x, y)))
            weight = sum([grid[vy][vx] for vx, vy in visited])

            new_head = heat + weight, x, y + delta, not step_vertical
            next_heads.append(new_head)
    else:  # step horizontal
        for delta in range(-limits[1], limits[1] + 1):
            if abs(delta) < limits[0] or not x_min <= x + delta <= x_max:
                continue

            visited = [(vx, y) for vx in range(min(x, x + delta), max(x, x + delta) + 1)]
            visited.pop(visited.index((x, y)))
            weight = sum([grid[vy][vx] for vx, vy in visited])

            new_head = heat + weight, x + delta, y, not step_vertical
            next_heads.append(new_head)

    return next_heads


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        grid = [line.strip() for line in puzzle.readlines()]

    for i in range(len(grid)):
        grid[i] = [int(tile) for tile in grid[i]]

    return grid


def solver(input_path, puzzle_type):
    assert puzzle_type in ('heat', 'ultra')

    limits = {'heat': (1, 3), 'ultra': (4, 10)}[puzzle_type]

    grid = loader(input_path)

    # TODO: use class to create objects
    heads = [
        # heat, x, y, next_vertical
        (0, 0, 0, True),
        (0, 0, 0, False),
    ]
    visited = set()

    end = len(grid[0]) - 1, len(grid) - 1

    while True:
        heads.sort()
        heat, x, y, next_vertical = heads.pop(0)

        if (x, y) == end:
            return heat

        if (x, y, next_vertical) in visited:
            continue

        visited.add((x, y, next_vertical))
        new_heads = step((heat, x, y, next_vertical), grid, limits)

        for new_head in new_heads:
            if new_head not in visited:
                heads.append(new_head)


def run_examples():
    examples = (
        ('test_input1', 'heat', 102),
        ('test_input1', 'ultra', 94),
        ('test_input2', 'ultra', 71),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'heat')
    part2 = solver('input', 'ultra')

    took = time.time() - start_time

    # print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 275000ms

    # Regression test
    assert part1 == 638
    assert part2 == 748


if __name__ == '__main__':
    run_examples()
    main()
