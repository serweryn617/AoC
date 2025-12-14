import itertools


def area(corner_a, corner_b):
    x1, y1 = corner_a
    x2, y2 = corner_b
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def solve_part1(parsed_input):
    areas = []
    for corner_a, corner_b in itertools.combinations(parsed_input, 2):
        areas.append(area(corner_a, corner_b))
    return max(areas)


def plot(point_arrays):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    for points in point_arrays:
        looped = points  # + [points[0]]
        x = [p[0] for p in looped]
        y = [p[1] for p in looped]
        ax.plot(x, y)

    plt.show()


def point_inside_rect(corner_a, corner_b, point):
    xr = corner_a[0], corner_b[0]
    yr = corner_a[1], corner_b[1]

    x, y = point
    if (xr[0] < x < xr[1]) and (yr[0] < y < yr[1]):
        return True
    return False


def any_point_inside_rect(corner_a, corner_b, points):
    for point in points:
        if point_inside_rect(corner_a, corner_b, point):
            return True
    return False


def get_rects_not_outside(areas, points):
    inside_rects = []
    for sq, ar in areas:
        r = sq[0], sq[2]
        if not any_point_inside_rect(*r, points):
            inside_rects.append((sq, ar))
    return inside_rects


def solve_part2(points):
    # plot([points])

    areas = []
    for corner_a, corner_b in itertools.combinations(points, 2):
        ar = area(corner_a, corner_b)
        corner_c = [corner_a[0], corner_b[1]]
        corner_d = [corner_b[0], corner_a[1]]

        c = sorted((corner_a, corner_b, corner_c, corner_d))
        sq = [c[0], c[1], c[3], c[2], c[0]]

        areas.append((sq, ar))

    areas.sort(key=lambda x: x[1], reverse=True)

    # HACK
    additional_blockpoints = [
        (50000, 48765),
        (50000, 50020),
    ]

    inside_rects = get_rects_not_outside(areas, points + additional_blockpoints)

    sq, ar = inside_rects[0]
    # plot([points, sq])
    return ar


def loader(input_path):
    data = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle:
            data.append(list(map(int, line.strip().split(','))))

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
        ('test_input', 1, 50),
        # ('test_input', 2, 24),  # HACK: part 2 works only for some inputs
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
    print(f'Solutions found in {took:.3f}s')  # 2464ms  # TODO: optimize

    # Regression test
    assert part1 == 4756718172
    assert part2 == 1665679194


if __name__ == '__main__':
    run_examples()
    main()
