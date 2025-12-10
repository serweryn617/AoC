def in_range(n, a, b):
    return a <= n <= b


def solve_part1(parsed_input):
    ranges, numbers = parsed_input

    fresh = 0
    for number in numbers:
        for a, b in ranges:
            if in_range(number, a, b):
                fresh += 1
                break

    return fresh


def overlaps(range_1, range_2):
    a1, b1 = range_1
    a2, b2 = range_2

    overlap_a = a1 <= a2 <= b1
    overlap_b = a1 <= b2 <= b1
    overlap_c = a2 <= a1 <= b2

    return overlap_a or overlap_b or overlap_c


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

    def count_inclusive(self):
        total = 0
        for s, e in self.ranges:
            total += e - s + 1
        return total


def solve_part2(parsed_input):
    ranges, _ = parsed_input

    mr = MultiRange()
    for r in ranges:
        mr.add(r)

    return mr.count_inclusive()


def loader(input_path):
    ranges = []
    numbers = []

    reached_numbers = False
    with open(input_path, 'r') as puzzle:
        for line in puzzle:
            l = line.strip()

            if not l:
                continue

            if '-' in l:
                a, b = l.split('-')
                ranges.append((int(a), int(b)))
            else:
                numbers.append(int(l))

    return ranges, numbers


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 3),
        ('test_input', 2, 14),
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
    print(f'Solutions found in {took:.3f}s')  # 6ms

    # Regression test
    assert part1 == 896
    assert part2 == 346240317247002


if __name__ == '__main__':
    run_examples()
    main()
