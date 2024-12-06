DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))


class Loop(Exception):
    pass


def get_visited(grid, start):
    dim = len(grid[0]), len(grid)

    visited = {}
    direction = 0
    pos = start

    while True:
        if pos not in visited:
            visited[pos] = [direction]
        elif direction not in visited[pos]:
            visited[pos].append(direction)
        else:
            raise Loop

        for _ in range(3):
            d = DIRECTIONS[direction]
            x, y = pos[0] + d[0], pos[1] + d[1]
            if 0 <= x < dim[0] and 0 <= y < dim[1] and grid[y][x] == '#':
                direction += 1
                direction %= len(DIRECTIONS)
            else:
                break

        pos = x, y

        if 0 > x or x >= dim[0] or 0 > y or y >= dim[1]:
            break

    return visited


def try_add_obstacle(grid, start, pos):
    new_grid = grid.copy()
    x, y = pos
    new_grid[y] = new_grid[y][:x] + '#' + new_grid[y][x + 1:]

    try:
        get_visited(new_grid, start)
    except Loop:
        print(pos)
        return True
    return False


def solve_part1(parsed_input):
    grid, start = parsed_input
    visited = get_visited(grid, start)

    return len(visited)


def solve_part2(parsed_input):
    grid, start = parsed_input
    visited = get_visited(grid, start)
    loops = 0

    # TODO: Better way than brute force?
    for pos in visited:
        loops += try_add_obstacle(grid, start, pos)

    return loops


def loader(input_path):
    grid = []
    
    with open(input_path, 'r') as puzzle:
        for y, line in enumerate(puzzle.readlines()):
            if '^' in line:
                start = (line.index('^'), y)
            grid.append(line.strip())

    return grid, start


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 41),
        ('test_input', 2, 6),
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
    print(f'Solutions found in {took:.3f}s')  # 3429ms

    # Regression test
    assert part1 == 4374
    assert part2 == 1705


if __name__ == '__main__':
    run_examples()
    main()
