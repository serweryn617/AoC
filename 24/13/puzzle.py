import re


def vec_div(av, bv):
    ax, ay = av
    bx, by = bv

    rx = ax / bx
    if rx % 1 != 0:
        return

    ry = ay / by
    if rx != ry:
        return 

    return int(rx)


def vec_sub(av, bv):
    ax, ay = av
    bx, by = bv
    return ax - bx, ay - by


class Machine:
    def __init__(self, va, vb, target):
        self.va = va
        self.vb = vb
        self.target = target

    def get_amounts(self):
        combinations = []

        pos = 0, 0
        target = self.target
        count_va = 0

        while pos[0] < target[0] and pos[1] < target[1]:
            div = vec_div(target, self.vb)
            if div:
                combinations.append((count_va, div))
            
            target = vec_sub(target, self.va)
            count_va += 1

        return combinations

    def offset_target(self, offset):
        self.target = self.target[0] + offset, self.target[1] + offset

    def crossing_point(self):
        Ax, Ay = self.va
        Bx, By = self.vb
        Tx, Ty = self.target

        # Derived equation for calculating x position of 2 crossing lines given:
        # - direction vector for line A and assuming it crosses (0,0)
        # - direction vector for line B
        # - point on line B
        num = Ax * Bx * Ty - Ax * By * Tx
        den = Ay * Bx - Ax * By
        crossing_x = num / den

        num_a = crossing_x / Ax
        num_b = (Tx - crossing_x) / Bx
        if num_a % 1 == 0 and num_b % 1 == 0:
            return int(num_a), int(num_b)


def weight_min(data, wa, wb):
    min_ = None

    for a, b in data:
        weight = a * wa + b * wb
        if min_ is None:
            min_ = weight
        min_ = min(min_, weight)

    return min_


def solve_part1(machines):
    total = 0

    for m in machines:
        possibilities = m.get_amounts()
        if not possibilities:
            continue
        min_ = weight_min(possibilities, 3, 1)
        total += min_

    return total


def solve_part2(machines):
    offset = 10000000000000
    total = 0

    for m in machines:
        m.offset_target(offset)
        # Since subtracting vectors is not allowed, there can be only one or no solution.
        # The case where vectors are parallel is not covered!
        point = m.crossing_point()

        if not point:
            continue

        total += point[0] * 3 + point[1]

    return total


def loader(input_path):
    machines = []

    with open(input_path, 'r') as puzzle:
        line = puzzle.readline().strip()
        while line:
            match = re.search(r'X+(.*), Y+(.*)', line)
            va = tuple(int(x) for x in match.groups())

            line = puzzle.readline().strip()
            match = re.search(r'X+(.*), Y+(.*)', line)
            vb = tuple(int(x) for x in match.groups())

            line = puzzle.readline().strip()
            match = re.search(r'X=(.*), Y=(.*)', line)
            target = tuple(int(x) for x in match.groups())

            puzzle.readline()
            line = puzzle.readline().strip()

            machines.append(Machine(va, vb, target))

    return machines


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 480),
        ('test_input', 2, 875318608908),
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
    print(f'Solutions found in {took:.3f}s')  # 10ms

    # Regression test
    assert part1 == 29187
    assert part2 == 99968222587852


if __name__ == '__main__':
    run_examples()
    main()
