class LensPuzzle:
    def __init__(self, num_boxes = 256):
        self.boxes = [{} for _ in range(num_boxes)]

    def add_lens(self, label, focal):
        box_num = hash_tm(label)
        self.boxes[box_num][label] = focal

    def remove_lens(self, label):
        box_num = hash_tm(label)
        if label in self.boxes[box_num]:
            self.boxes[box_num].pop(label)

    def solve(self, steps):
        for step in steps:
            t = step.split('=')
            if len(t) == 2:
                self.add_lens(t[0], int(t[1]))
            else:
                self.remove_lens(step[:-1])

        total = 0

        for box_num, box in enumerate(self.boxes):
            for slot, focal in enumerate(box.values()):
                total += (box_num + 1) * (slot + 1) * focal

        return total


def hash_tm(step):
    val = 0

    for c in step:
        val += ord(c)
        val *= 17
        val %= 256

    return val


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        steps = puzzle.readline().strip().split(',')

    return steps


def solver(input_path, puzzle_type):
    assert puzzle_type in ('hash', 'lens')

    steps = loader(input_path)

    if puzzle_type == 'hash':
        return sum(map(hash_tm, steps))
    else:
        return LensPuzzle().solve(steps)


def run_examples():
    examples = (
        ('test_input', 'hash', 1320),
        ('test_input', 'lens', 145),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'hash')
    part2 = solver('input', 'lens')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 3ms

    # Regression test
    assert part1 == 519041
    assert part2 == 260530


if __name__ == '__main__':
    run_examples()
    main()
