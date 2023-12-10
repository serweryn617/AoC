TILES_TOP = {
    '|': 't',
    '7': 'l',
    'F': 'r',
}

TILES_BOTTOM = {
    '|': 'b',
    'L': 'r',
    'J': 'l',
}

TILES_LEFT = {
    '-': 'l',
    'L': 't',
    'F': 'b',
}

TILES_RIGHT = {
    '-': 'r',
    'J': 't',
    '7': 'b',
}


def dir_delta(d):
    if d == 't':
        return -1, 0
    elif d == 'b':
        return 1, 0
    elif d == 'l':
        return 0, -1
    elif d == 'r':
        return 0, 1


def get_start_pos(grid):
    for y, line in enumerate(grid):
        x = line.find('S')
        if x != -1:
            break
    else:
        assert False, 'Starting position not found!'

    top = grid[y - 1][x]
    bottom = grid[y + 1][x]
    left = grid[y][x - 1]
    right = grid[y][x + 1]

    # Loop enterances:
    start_tiles = []

    if top in TILES_TOP:
        dnext = 't'
        start_tiles.append({
            'pos': [y, x],
            'next': dnext
        })
    if bottom in TILES_BOTTOM:
        dnext = 'b'
        start_tiles.append({
            'pos': [y, x],
            'next': dnext
        })
    if left in TILES_LEFT:
        dnext = 'l'
        start_tiles.append({
            'pos': [y, x],
            'next': dnext
        })
    if right in TILES_RIGHT:
        dnext = 'r'
        start_tiles.append({
            'pos': [y, x],
            'next': dnext
        })

    return start_tiles, (y, x)


def get_next_pos_from_dir(pos, next_dir):
    dy, dx = dir_delta(next_dir)
    y = pos[0] + dy
    x = pos[1] + dx
    return y, x


def mark_loop_tile(grid, pos):
    y, x = pos
    current_tile = grid[y][x]
    if current_tile in '7F':
        replace_tile(grid, y, x, 'd')
    elif current_tile in 'JL':
        replace_tile(grid, y, x, 'u')
    elif current_tile == '|':
        replace_tile(grid, y, x, 'x')


def traverse_loop(grid, starts, mark=True):
    assert len(starts) == 2, 'Loop must have 2 starting positions!'

    distance = 0

    while True:
        for i, s in enumerate(starts):
            ynext, xnext = get_next_pos_from_dir(s['pos'], s['next'])
            tile = grid[ynext][xnext]

            if s['next'] == 't' and tile in TILES_TOP:
                dnext = TILES_TOP[tile]
            elif s['next'] == 'b' and tile in TILES_BOTTOM:
                dnext = TILES_BOTTOM[tile]
            elif s['next'] == 'l' and tile in TILES_LEFT:
                dnext = TILES_LEFT[tile]
            elif s['next'] == 'r' and tile in TILES_RIGHT:
                dnext = TILES_RIGHT[tile]

            starts[i]['pos'] = [ynext, xnext]
            starts[i]['next'] = dnext

            if mark:
                mark_loop_tile(grid, s['pos'])

        distance += 1

        # Is it always valid for square grid?
        if starts[0]['pos'] == starts[1]['pos']:
            return distance


def replace_tile(grid, y, x, new_tile):
    grid[y] = grid[y][:x] + new_tile + grid[y][x + 1:]


def start_tile_type(starts):
    dir0 = starts[0]['next']
    dir1 = starts[1]['next']
    dirs = sorted(dir0 + dir1)
    dirs = dirs[0] + dirs[1]

    replace_char = '-'
    if dirs in ('bt',):
        replace_char = 'x'
    elif dirs in ('br', 'bl'):
        replace_char = 'd'
    elif dirs in ('rt', 'lt'):
        replace_char = 'u'

    return replace_char


def get_enclosed_area(grid):
    # Iterate over tiles starting from the edge, count how many times the loop was crossed
    # Odd number of crossings means tile is enclosed by the loop

    def check_if_crossed():
        nonlocal crossings, up, down
        if up and down:
            crossings += 1
            up, down = 0, 0

    inside = 0

    for line in grid:
        crossings, up, down = 0, 0, 0

        for tile in line:
            if tile == 'x':
                crossings += 1
            elif tile == 'u':
                up ^= 1
                check_if_crossed()
            elif tile == 'd':
                down ^= 1
                check_if_crossed()
            elif not up and not down and crossings % 2 == 1:
                inside += 1

    return inside


def solver(input_path):
    with open(input_path, 'r') as puzzle:
        grid = [line.rstrip() for line in puzzle.readlines()]

    starts, (ys, xs) = get_start_pos(grid)
    start_replace_tile = start_tile_type(starts)
    replace_tile(grid, ys, xs, start_replace_tile)

    loop_max_distance = traverse_loop(grid, starts)
    area_inside_loop = get_enclosed_area(grid)

    return loop_max_distance, area_inside_loop


def run_examples():
    examples = (
        ('test_input_1a', 0, 4),
        ('test_input_1b', 0, 4),
        ('test_input_1c', 0, 8),
        ('test_input_1d', 0, 8),
        ('test_input_2a', 1, 4),
        ('test_input_2b', 1, 4),
        ('test_input_2c', 1, 8),
        ('test_input_2d', 1, 10),
    )

    for path, mode, expected in examples:
        result = solver(path)[mode]
        assert result == expected, f'Example {path} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1, part2 = solver('input')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 7ms

    # Regression test
    assert part1 == 6806
    assert part2 == 449


if __name__ == '__main__':
    run_examples()
    main()

































