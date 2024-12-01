from time import sleep


PRINT = False
SAND = 500, 0


def show(formations):
    width = min(formations, key=lambda p: p[0])[0], max(formations, key=lambda p: p[0])[0]
    height = min(formations, key=lambda p: p[1])[1], max(formations, key=lambda p: p[1])[1]

    print('Rock formations:')
    sleep(0.1)
    for y in range(*height):
        for x in range(*width):
            if (x, y) in formations:
                c = formations[(x, y)]
            else:
                c = '.'
            print(c, end='')
        print()


def populate(formations, rocks_lines):
    for rock_line in rocks_lines:
        starting_point = rock_line[0]
        for r in rock_line[1:]:
            populate_line(formations, starting_point, r)
            starting_point = r


def populate_line(formations, start, end):
    if start[0] == end[0]:
        sy = min(start[1], end[1])
        ey = max(start[1], end[1])
        points = ((start[0], y) for y in range(sy, ey + 1))
    else:
        sx = min(start[0], end[0])
        ex = max(start[0], end[0])
        points = ((x, start[1]) for x in range(sx, ex + 1))

    for p in points:
        formations[p] = '#'


def add_sand(formations, max_depth, *, floor=False):
    sand = list(SAND)
    solidify = False

    while not solidify:
        if (sand[0], sand[1] + 1) not in formations:
            sand[1] += 1
        elif (sand[0] - 1, sand[1] + 1) not in formations:
            sand[0] -= 1
            sand[1] += 1
        elif (sand[0] + 1, sand[1] + 1) not in formations:
            sand[0] += 1
            sand[1] += 1
        else:
            solidify = True

        if sand[1] == max_depth:
            if floor:
                solidify = True
            else:
                return False

    formations[tuple(sand)] = 'o'
    return True


def solve_part1(parsed_input):
    formations = {}
    populate(formations, parsed_input)
    max_depth = max(formations, key=lambda p: p[1])[1]

    total_sand = 0
    while add_sand(formations, max_depth):
        total_sand += 1

        if PRINT: show(formations)

    return total_sand

def solve_part2(parsed_input):
    formations = {}
    populate(formations, parsed_input)
    max_depth = max(formations, key=lambda p: p[1])[1]
    max_depth += 1

    total_sand = 0
    while SAND not in formations:
        add_sand(formations, max_depth, floor=True)
        total_sand += 1

        if PRINT: show(formations)

    return total_sand


def loader(input_path):
    rocks = []

    def split(rock_str):
        x, y = rock_str.split(',')
        return int(x), int(y)

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            line = line.strip().split(' -> ')
            r = [split(l) for l in line]
            rocks.append(r)

    return rocks


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 24),
        ('test_input', 2, 93),
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
    print(f'Solutions found in {took:.3f}s')  # 411ms

    # Regression test
    assert part1 == 757
    assert part2 == 24943


if __name__ == '__main__':
    run_examples()
    main()
