import re


class MultiRange:
    def __init__(self):
        self.ranges = []

    def add(self, r):
        assert len(r) == 2

        self.ranges.append(r)
        self.ranges.sort()

        while True:
            for b in range(1, len(self.ranges)):
                a = b - 1
                start_a, end_a = self.ranges[a]
                start_b, end_b = self.ranges[b]

                if start_b <= (end_a + 1):
                    self.ranges[a] = start_a, max(end_a, end_b)
                    self.ranges.pop(b)
                    break
            else:
                return

    def count(self):
        total = 0
        for s, e in self.ranges:
            total += e - s
        return total

    def limit_to(self, limit):
        start, end = limit

        self.ranges = list(filter(lambda x: x[0] <= end, self.ranges))
        self.ranges[-1] = self.ranges[-1][0], min(self.ranges[-1][1], end)

        self.ranges = list(filter(lambda x: x[1] >= start, self.ranges))
        self.ranges[0] = max(self.ranges[0][0], start), self.ranges[0][1]

class Sensor:
    def __init__(self, pos, beacon):
        self.pos = pos
        self.beacon = beacon
        self.dist = abs(pos[0] - beacon[0]) + abs(pos[1] - beacon[1])

    def get_range_at_y(self, y):
        y_diff = abs(self.pos[1] - y)
        left = self.dist - y_diff
        if left >= 0:
            return self.pos[0] - left, self.pos[0] + left


def solve_part1(sensors, is_example):
    if is_example:
        row = 10
    else:
        row = 2000000
    
    mr = MultiRange()

    for s in sensors:
        r = s.get_range_at_y(row)
        if r:
            mr.add(r)

    return mr.count()


def solve_part2(sensors, is_example):
    if is_example:
        max_y = 20
    else:
        max_y = 4000000

    mul = 4000000

    # TODO: this takes close to 30 seconds, is there a better way to get the answer?
    for y in range(max_y):
        mr = MultiRange()

        for s in sensors:
            r = s.get_range_at_y(y)
            if r:
                mr.add(r)

        mr.limit_to((0, max_y))
        if mr.count() != max_y:
            break

    x = mr.ranges[0][1] + 1
    return x * mul + y


def loader(input_path):
    sensors = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            match = re.search(r'Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)', line)
            sx, sy, bx, by = tuple(int(x) for x in match.groups())
            sensors.append(Sensor((sx, sy), (bx, by)))

    return sensors


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 26),
        ('test_input', 2, 56000011),
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
    print(f'Solutions found in {took:.3f}s')  # 26910ms

    # Regression test
    assert part1 == 4883971
    assert part2 == 12691026767556


if __name__ == '__main__':
    run_examples()
    main()
