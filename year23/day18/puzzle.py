DIG_DIR_DELTA = {
    'L': (0, -1),
    'R': (0, 1),
    'U': (-1, 0),
    'D': (1, 0),
}

HEX_DIR = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}


def concave_polygon_area(corners):
    # sum of cross products
    area = 0

    for i in range(len(corners)):
        y0, x0 = corners[i - 1]  # wraps in the first iteration
        y1, x1 = corners[i]
        area += x0 * y1 - x1 * y0

    return abs(area / 2)


def get_corners(data):
    y, x = 0, 0
    corners = [(y, x)]

    for direction, length in data:
        dy, dx = DIG_DIR_DELTA[direction]

        y += dy * length
        x += dx * length
        corners.append((y, x))

    return corners


def num_edge_tiles(data):
    return sum(length for _, length in data)


def loader(input_path, use_hex_data = False):
    puzzle_input = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            dig_dir, dig_len, hex_data = line.split()
            dig_len = int(dig_len)
            hex_distance = int(hex_data[2:-2], base=16)
            hex_dir = HEX_DIR[hex_data[-2]]

            if use_hex_data:
                puzzle_input.append((hex_dir, hex_distance))
            else:
                puzzle_input.append((dig_dir, dig_len))

    return puzzle_input


def solver(input_path, puzzle_type):
    assert puzzle_type in ('lagoon', 'hex')

    dig_data = loader(input_path, puzzle_type == 'hex')

    corners = get_corners(dig_data)

    area = concave_polygon_area(corners)
    edge_len = num_edge_tiles(dig_data)

    # half of each tile, +1 for completing a loop
    missing_area = edge_len // 2 + 1

    return int(area) + missing_area


def run_examples():
    examples = (
        ('test_input', 'lagoon', 62),
        ('test_input', 'hex', 952408144115),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'lagoon')
    part2 = solver('input', 'hex')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # <1ms

    # Regression test
    assert part1 == 50746
    assert part2 == 70086216556038


if __name__ == '__main__':
    run_examples()
    main()
