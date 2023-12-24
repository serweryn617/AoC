class Hailstone:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def collides_with_2d(self, hailstone):
        x1, y1, _ = self.vel
        x2, y2, _ = hailstone.vel

        cross_prod = x1 * y2 - x2 * y1
        return bool(cross_prod)

    def intersection_point_2d(self, hailstone):
        # TODO: try using parametric equations
        x1, y1, _ = self.pos
        dx1, dy1, _ = self.vel

        x2, y2, _ = hailstone.pos
        dx2, dy2, _ = hailstone.vel

        # Assume no division by 0
        a1 = dy1 / dx1
        a2 = dy2 / dx2

        b1 = y1 - a1 * x1
        b2 = y2 - a2 * x2

        px = (b2 - b1) / (a1 - a2)
        py = a1 * px + b1

        return px, py

    def point_in_future_2d(self, point):
        px, py = point
        x, y, _ = self.pos
        vx, vy, _ = self.vel

        dx = px - x
        dy = py - y

        # Assume no rocks with velocity 0
        mx = dx / vx
        my = dy / vy

        return mx >= 0 and my >= 0


def hailstones_intersect_2d(a, b, limits):
    if not a.collides_with_2d(b):
        return False

    px, py = a.intersection_point_2d(b)

    if limits[0] <= px <= limits[1] and limits[0] <= py <= limits[1]:
        if a.point_in_future_2d((px, py)) and b.point_in_future_2d((px, py)):
            return True

    return False


def loader(input_path):
    hailstones = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            pos, vel = line.split('@')
            pos = tuple(map(int, pos.split(',')))
            vel = tuple(map(int, vel.split(',')))
            hailstones.append(Hailstone(pos, vel))

    return hailstones


def solver(input_path, puzzle_type, limits):
    assert puzzle_type in ('2d', 'longest')

    hailstones = loader(input_path)

    intersections = 0
    for i in range(len(hailstones) - 1):
        for j in range(i + 1, len(hailstones)):
            if hailstones_intersect_2d(hailstones[i], hailstones[j], limits):
                intersections += 1

    return intersections


def run_examples():
    examples = (
        ('test_input', '2d', (7, 27), 2),
        # ('test_input', 'rock', (), 47),
    )

    for path, puzzle_type, limits, expected in examples:
        result = solver(path, puzzle_type, limits)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', '2d', (200000000000000, 400000000000000))
    # part2 = solver('input', 'rock', ())

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    # print('Puzzle 2 answer:', part2)
    print(f'Solution found in {took:.3f}s')  # 26ms

    # Regression test
    assert part1 == 16589
    # assert part2 == 


if __name__ == '__main__':
    run_examples()
    main()
