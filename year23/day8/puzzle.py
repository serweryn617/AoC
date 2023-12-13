from math import lcm


def traverse_camels(directions, maps):
    key = 'AAA'
    target = 'ZZZ'
    num_steps = 0

    while True:
        for d in directions:
            if key == target:
                return num_steps

            key = maps[key][d]
            num_steps += 1


def get_repeats(key, directions, maps):
    visited = {}  # using dict is way faster than list
    num_steps = 0

    while True:
        for dir_num, d in enumerate(directions):
            if (key, dir_num) in visited:
                initial = visited[(key, dir_num)]
                loop = num_steps - initial
                return initial, loop

            visited[(key, dir_num)] = num_steps

            key = maps[key][d]
            num_steps += 1


def traverse_ghosts(directions, maps):
    keys = [key for key in maps if key[-1] == 'A']
    loops = []
    initials = []

    for k in keys:
        init, loop = get_repeats(k, directions, maps)
        loops.append(loop)
        initials.append(init)

    # Assume:
    # - there is 1 target at location A
    # - ghost paths loop with period A, target is contained in this loop
    # Invalid for puzzle example 2 (therefore, no checks in the code)
    # Valid for my puzzle input
    # TODO: How to generalize the solver?
    return lcm(*loops)


def solver(input_path, puzzle_type: str):
    assert puzzle_type in ('camels', 'ghosts')

    maps = {}

    with open(input_path, 'r') as puzzle:
        directions = puzzle.readline().strip()
        puzzle.readline()

        for line in puzzle.readlines():
            key = line[:3]
            left = line[7:10]
            right = line[12:15]

            maps[key] = {'L': left, 'R': right}

    if puzzle_type == 'camels':
        num_steps = traverse_camels(directions, maps)
    else:
        num_steps = traverse_ghosts(directions, maps)

    return num_steps


def run_examples():
    examples = (
        ('test_input1', 'camels', 6),
        ('test_input2', 'ghosts', 6),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} failed: {result}'

    print('Examples passed')


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'camels')
    part2 = solver('input', 'ghosts')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 17ms

    # Regression test
    assert part1 == 16697
    assert part2 == 10668805667831


if __name__ == '__main__':
    run_examples()
    main()
