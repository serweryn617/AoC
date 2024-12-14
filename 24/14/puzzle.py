import re


class Robot:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
    
    def set_bound(self, bound):
        self.bound = bound

    def move(self, seconds):
        x = self.pos[0] + self.vel[0] * seconds
        y = self.pos[1] + self.vel[1] * seconds

        x %= self.bound[0]
        y %= self.bound[1]

        self.pos = x, y

    def quad(self):
        mid_x = self.bound[0] // 2
        mid_y = self.bound[1] // 2

        if self.pos[0] == mid_x or self.pos[1] == mid_y:
            return

        return self.pos[0] < mid_x, self.pos[1] < mid_y


def solve_part1(robots, is_example):
    if is_example:
        bound = (11, 7)
    else:
        bound = (101, 103)

    quads = {(0,0): 0, (0,1): 0, (1,0): 0, (1,1): 0}
    for r in robots:
        r.set_bound(bound)
        r.move(100)
        q = r.quad()
        if q:
            quads[q] += 1

    a, b, c, d = quads.values()
    return a * b * c * d


def print_robots(robots, bound):
    pos = {}
    for r in robots:

        if r.pos not in pos:
            pos[r.pos] = 1
        else:
            pos[r.pos] += 1

    for y in range(bound[1]):
        for x in range(bound[0]):
            if (x, y) in pos:
                print('X', end='')
            else:
                print('.', end='')
        print()
    print('Do you see a christmas tree?')


def solve_part2(robots, is_example):
    if is_example:
        bound = (11, 7)
    else:
        bound = (101, 103)

    most = len(robots) // 2

    for i in range(1, 100000):
        quads = {(0,0): 0, (0,1): 0, (1,0): 0, (1,1): 0}
        for r in robots:
            r.set_bound(bound)
            r.move(1)
            q = r.quad()
            if q:
                quads[q] += 1

        # TODO: hope most of the robots will be in one quadrant
        if any(map(lambda x: x > most, quads.values())):
            print_robots(robots, bound)
            return i


def loader(input_path):
    robots = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            match = re.search(r'p=(.*),(.*) v=(.*),(.*)', line)
            px, py, vx, vy = tuple(int(x) for x in match.groups())
            robots.append(Robot((px, py), (vx, vy)))

    return robots


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 12),
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
    print(f'Solutions found in {took:.3f}s')  # 1106ms

    # Regression test
    assert part1 == 229069152
    assert part2 == 7383


if __name__ == '__main__':
    run_examples()
    main()
