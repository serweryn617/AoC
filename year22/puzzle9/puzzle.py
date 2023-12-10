


# def expand_grid(grid: list[list], direction, pattern = False):
#     if direction == 'L':
#         for row in grid:
#             row.insert(0, pattern)
#     if direction == 'R':
#         for row in grid:
#             row.append(pattern)
#     if direction == 'U':
#         grid.insert(0, [pattern for _ in grid[0]])
#     if direction == 'D':
#         grid.append([pattern for _ in grid[0]])


def move_head(head_pos, direction):
    if direction == 'L':
        head_pos[0] -= 1
    if direction == 'R':
        head_pos[0] += 1
    if direction == 'U':
        head_pos[1] -= 1
    if direction == 'D':
        head_pos[1] += 1


def move_tail(head, tail):
    dx = head[0] - tail[0] + 2
    dy = head[1] - tail[1] + 2

    lut = (
        ((-1, -1), (-1, -1), ( 0, -1), ( 1, -1), ( 1, -1)),
        ((-1, -1), ( 0,  0), ( 0,  0), ( 0,  0), ( 1, -1)),
        ((-1,  0), ( 0,  0), ( 0,  0), ( 0,  0), ( 1,  0)),
        ((-1,  1), ( 0,  0), ( 0,  0), ( 0,  0), ( 1,  1)),
        ((-1,  1), (-1,  1), ( 0,  1), ( 1,  1), ( 1,  1)),
    )

    tail[0] += lut[dy][dx][0]
    tail[1] += lut[dy][dx][1]


def update_positions(positions, knot):
    positions[f'{knot[0]},{knot[1]}'] = True


def printer(positions, knots):
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for key in positions:
        x, y = key.split(',')
        x = int(x)
        y = int(y)

        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    min_x -= len(knots)
    min_y -= len(knots)
    max_x += len(knots) + 1
    max_y += len(knots) + 1

    print('')
    print('PRINTER')
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if knots[0] == [x, y]:
                print('H', end='')
            elif knots[-1] == [x, y]:
                print('T', end='')
            elif [x,y] in knots:
                print('X', end='')
            elif f'{x},{y}' in positions and positions[f'{x},{y}']:
                print('*', end='')
            else:
                print('.', end='')
        print('')


def solver(input_path, knots_num):
    knots = [[0, 0] for _ in range(knots_num + 1)]
    positions = {}

    update_positions(positions, knots[-1])

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            direction, length = line.strip().split()
            length = int(length)

            for _ in range(length):
                move_head(knots[0], direction)
                for k in range(knots_num):
                    move_tail(knots[k], knots[k + 1])
                update_positions(positions, knots[-1])
                # printer(positions, knots)

    return len(positions)


if __name__ == '__main__':
    expected1 = 13
    result1 = solver('test_input1', 1)
    assert result1 == expected1, f'Example 1 failed: {result1}'

    expected2 = 36
    result2 = solver('test_input2', 9)
    assert result2 == expected2, f'Example 2 failed: {result2}'

    print("Examples passed")
    print("Puzzle 1 answer:", solver('input', 1))
    print("Puzzle 2 answer:", solver('input', 9))

