class Brick:
    def __init__(self, descriptor):
        self._brick_from_string(descriptor)
        self.on_top = []
        self.below = []

    def _brick_from_string(self, descriptor):
        start, end = descriptor.strip().split('~')
        sx, sy, sz = map(int, start.split(','))
        ex, ey, ez = map(int, end.split(','))

        self.x = sorted((sx, ex))
        self.y = sorted((sy, ey))
        self.z = sorted((sz, ez))

    def get_z(self):
        return self.z

    def get_z_top(self):
        return self.z[1]

    def move_to_z(self, z):
        height = self.z[1] - self.z[0]
        self.z = z, z + height

    def will_collide_with(self, brick):
        x_condition = brick.x[1] >= self.x[0] and brick.x[0] <= self.x[1]
        y_condition = brick.y[1] >= self.y[0] and brick.y[0] <= self.y[1]

        return x_condition and y_condition

    def collision_height(self):
        return self.z[1] + 1

    def add_on_top(self, brick):
        self.on_top.append(brick)

    def add_below(self, bricks):
        self.below += bricks


def drop_bricks(bricks):
    bricks.sort(key=Brick.get_z)

    for n, brick in enumerate(bricks):
        min_height = 0
        foundations = []

        for supp in reversed(bricks[:n]):
            if brick.will_collide_with(supp):
                height = supp.collision_height()
                if height > min_height:
                    min_height = height
                    foundations = [supp]
                elif height == min_height:
                    foundations.append(supp)

        brick.move_to_z(min_height)
        brick.add_below(foundations)

        for supp in foundations:
            supp.add_on_top(brick)


def is_safely_removable(brick):
    # None on top
    if len(brick.on_top) == 0:
        return True

    # All on top are supported by at least 1 other brick
    if all([len(b.below) > 1 for b in brick.on_top]):
        return True

    return False


def num_safely_removable(bricks):
    removable = 0

    for brick in bricks:
        if is_safely_removable(brick):
            removable += 1

    return removable


def total_fell(bricks):
    total = 0

    for brick in bricks:
        if is_safely_removable(brick):
            continue

        # this part could be cleaner
        fell = [brick]
        while fell:

            for check in fell[0].on_top:
                # duplicates in 'fell' will be automatically rejected here
                if set(check.below) <= set(fell):
                    fell.append(check)
                    total += 1

            fell.pop(0)
            fell.sort(key=Brick.get_z_top)

    return total


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        bricks = [Brick(descriptor) for descriptor in puzzle.readlines()]

    return bricks


def solver(input_path, puzzle_type):
    assert puzzle_type in ('least', 'most')

    bricks = loader(input_path)
    drop_bricks(bricks)

    if puzzle_type == 'least':
        puzzle_answer = num_safely_removable(bricks)
    else:
        puzzle_answer = total_fell(bricks)

    return puzzle_answer


def run_examples():
    examples = (
        ('test_input', 'least', 5),
        ('test_input', 'most', 7),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'least')
    part2 = solver('input', 'most')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Solution found in {took:.3f}s')  # 180ms

    # Regression test
    assert part1 == 398
    assert part2 == 70727


if __name__ == '__main__':
    run_examples()
    main()
