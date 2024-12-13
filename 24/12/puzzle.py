DIRECTIONS = {(1, 0): 'L', (-1, 0): 'R', (0, 1): 'D', (0, -1): 'U'}


def fill_region(region, pos, match, grid, visited, in_region):
    mx = len(grid[0])
    my = len(grid)
    x, y = pos

    if x < 0 or x >= mx or y < 0 or y >= my:
        return

    if visited[y][x] == True or in_region[y][x] == True:
        return

    visited[y][x] = True
    if grid[y][x] == match:
        region.append((x, y))
        in_region[y][x] = True
    else:
        return

    for dx, dy in DIRECTIONS:
        next_pos = x + dx, y + dy
        fill_region(region, next_pos, match, grid, visited, in_region)


def get_regions(grid):
    len_x = len(grid[0])
    len_y = len(grid)
    in_region = [[0 for _ in range(len_x)] for _ in range(len_y)]

    regions = []
    for y in range(len_y):
        for x in range(len_x):
            visited = [[0 for _ in range(len_x)] for _ in range(len_y)]
            region = []
            match = grid[y][x]
            fill_region(region, (x, y), match, grid, visited, in_region)
            if region:
                regions.append(region)

    return regions


def calc_outline(region):
    outline = {}

    for tile in region:
        x, y = tile
        for (dx, dy), d in DIRECTIONS.items():
            neighbour = x + dx, y + dy
            if neighbour not in region:
                outline[(x * 2 + dx, y * 2 + dy)] = d

    return outline


def solve_part1(grid):
    regions = get_regions(grid)
    total = 0

    for region in regions:
        outline = len(calc_outline(region))
        area = len(region)
        total += area * outline

    return total


# TODO: do this better
def num_corners(p, points):
    offsets = (-1, -1), (1, -1), (-1, 1), (1, 1)

    x, y = p
    diags = [(x + dx, y + dy) for dx, dy in offsets]
    present = (bool(x in points) for x in diags)

    vals = []
    for d in diags:
        if d in points:
            vals.append(points[d])
        else:
            vals.append(None)

    count = sum(present)

    up = vals[0], vals[1]
    if ('U' in up and 'D' in up):
        count -= 1
    down = vals[2], vals[3]
    if ('U' in down and 'D' in down):
        count -= 1
    left = vals[0], vals[2]
    if ('L' in left and 'R' in left):
        count -= 1
    right = vals[1], vals[3]
    if ('L' in right and 'R' in right):
        count -= 1

    return count


def count_straights(points):
    total = 0

    for p in points:
        total += num_corners(p, points)

    assert total % 2 == 0
    return total // 2


def solve_part2(grid):
    regions = get_regions(grid)
    total = 0

    for region in regions:
        outline_points = calc_outline(region)
        outline = count_straights(outline_points)

        area = len(region)
        total += area * outline

    return total


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        grid = [line.strip() for line in puzzle.readlines()]

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
        ('test_input', 1, 140),
        ('test_input1', 1, 772),
        ('test_input2', 1, 1930),

        ('test_input', 2, 80),
        ('test_input1', 2, 436),
        ('test_input2', 2, 1206),
        ('test_input3', 2, 236),
        ('test_input4', 2, 368),
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
    print(f'Solutions found in {took:.3f}s')  # 6140ms

    # Regression test
    assert part1 == 1396562
    assert part2 == 844132


if __name__ == '__main__':
    run_examples()
    main()
