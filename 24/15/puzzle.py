ROBOT = '@'
BOX = 'O'
WALL = '#'
EMPTY = '.'

DIRECTIONS = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1),
}


def get_char_pos(grid, char):
    for y, row in enumerate(grid):
        if char in row:
            return row.index(char), y


def to_pos_dict(grid):
    pos_dict = {}
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            pos_dict[(x, y)] = char
    return pos_dict


def vec_add(va, vb):
    return va[0] + vb[0], va[1] + vb[1]


def first_empty(pos, direction, grid):
    while True:
        pos = vec_add(pos, direction)
        x, y = pos
        char = grid[(x, y)]
        if char == WALL:
            return
        elif char != BOX:
            return x, y


def push(robot, direction, grid):
    empty = first_empty(robot, direction, grid)
    if empty:
        robot = vec_add(robot, direction)
        grid[robot] = EMPTY

        if empty != robot:
            grid[empty] = BOX

    return robot


def calc_gps(grid):
    total = 0
    for key, val in grid.items():
        if val != BOX:
            continue
        
        x, y = key
        total += 100 * y + x
    return total


def solve_part1(parsed_input, is_example):
    grid, moves = parsed_input
    robot = get_char_pos(grid, ROBOT)
    pos_dict = to_pos_dict(grid)
    pos_dict[robot] = EMPTY

    for m in moves:
        d = DIRECTIONS[m]
        robot = push(robot, d, pos_dict)

    return calc_gps(pos_dict)


def adjust(grid):
    new_grid = []
    for line in grid:
        line = line.replace('.', '..')
        line = line.replace('O', 'O.')
        line = line.replace('@', '@.')
        line = line.replace('#', '##')
        new_grid.append(line)
    return new_grid


def can_push_box(box_pos, d, pos_dict):
    wall_offsets = {
        (1, 0): ((2, 0),),
        (-1, 0): ((-1, 0),),
        (0, 1): ((0, 1), (1, 1)),
        (0, -1): ((0, -1), (1, -1)),
    }
    walls = wall_offsets[d]
    for wall in walls:
        wall = vec_add(box_pos, wall)
        if pos_dict[wall] == WALL:
            return False

    wide_box_offsets = {
        (1, 0): ((2, 0),),
        (-1, 0): ((-2, 0),),
        (0, 1): ((-1, 1), (0, 1), (1, 1)),
        (0, -1): ((-1, -1), (0, -1), (1, -1)),
    }
    offsets = wide_box_offsets[d]
    for offset in offsets:
        next_box = vec_add(box_pos, offset)
        if pos_dict[next_box] != BOX:
            continue
        ok = can_push_box(next_box, d, pos_dict)
        if not ok:
            return False

    return True


def push_boxes(box_pos, d, pos_dict):
    wide_box_offsets = {
        (1, 0): ((2, 0),),
        (-1, 0): ((-2, 0),),
        (0, 1): ((-1, 1), (0, 1), (1, 1)),
        (0, -1): ((-1, -1), (0, -1), (1, -1)),
    }
    offsets = wide_box_offsets[d]
    for offset in offsets:
        next_box = vec_add(box_pos, offset)
        if pos_dict[next_box] == BOX:
            push_boxes(next_box, d, pos_dict)
    next_pos = vec_add(box_pos, d)
    pos_dict[box_pos] = EMPTY
    pos_dict[next_pos] = BOX


WIDE_BOX_ROBOT_OFFSETS = {
    '>': ((1, 0),),
    '<': ((-2, 0),),
    'v': ((-1, 1), (0, 1)),
    '^': ((-1, -1), (0, -1)),
}


def solve_part2(parsed_input, is_example):
    grid, moves = parsed_input
    grid = adjust(grid)
    pos_dict = to_pos_dict(grid)
    robot = get_char_pos(grid, ROBOT)
    pos_dict[robot] = EMPTY

    for r in grid:
        print(r)

    for m in moves:
        d = DIRECTIONS[m]
        next_pos = vec_add(robot, d)
        if pos_dict[next_pos] == WALL:
            continue

        offsets = WIDE_BOX_ROBOT_OFFSETS[m]
        for offset in offsets:
            box_pos = vec_add(robot, offset)
            if pos_dict[box_pos] != BOX:
                continue

            ok = can_push_box(box_pos, d, pos_dict)
            if ok:
                push_boxes(box_pos, d, pos_dict)
                robot = next_pos
            break
        else:
            robot = next_pos

    return calc_gps(pos_dict)


def loader(input_path):
    grid = []
    moves = ''

    with open(input_path, 'r') as puzzle:
        line = puzzle.readline().strip()
        while line:
            grid.append(line)
            line = puzzle.readline().strip()

        line = puzzle.readline().strip()
        while line:
            moves += line
            line = puzzle.readline().strip()

    return grid, moves


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 2028),
        ('test_input2', 1, 10092),
        ('test_input2', 2, 9021),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type, is_example=True)
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
    print(f'Solutions found in {took:.3f}s')  # 7ms

    # Regression test
    assert part1 == 1497888
    assert part2 == 1522420


if __name__ == '__main__':
    run_examples()
    main()
