from math import ceil, floor


def get_hold_times(time, distance):
    d = (time ** 2 - 4 * distance) ** 0.5
    x1 = (time - d) / 2
    x2 = (time + d) / 2

    # Distance must be strictly greater than the record to win (>= is not enough)
    # Assume x1 < x2
    x1 = x1 if x1 % 1 else x1 + 1
    x2 = x2 if x2 % 1 else x2 - 1

    return range(ceil(x1), floor(x2) + 1)


def solver(input_path, puzzle_type: str):
    assert puzzle_type in ('margin', 'single')

    puzzle_answer = 1

    with open(input_path, 'r') as puzzle:
        if puzzle_type == 'single':
            time = puzzle.readline().split(':')[1].replace(' ', '')
            time = [int(time)]

            distance = puzzle.readline().split(':')[1].replace(' ', '')
            distance = [int(distance)]
        else:
            time = [int(i) for i in puzzle.readline().split()[1:]]
            distance = [int(i) for i in puzzle.readline().split()[1:]]

    for t, d in zip(time, distance):
        hold = get_hold_times(t, d)
        puzzle_answer *= len(hold)

    return puzzle_answer


def run_examples():
    examples = (
        ('test_input', 'margin', 288),
        ('test_input', 'single', 71503),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} failed: {result}'

    print('Examples passed')


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'margin')
    part2 = solver('input', 'single')
    
    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # <1ms

    # Regression test
    assert part1 == 2269432
    assert part2 == 35865985


if __name__ == '__main__':
    run_examples()
    main()