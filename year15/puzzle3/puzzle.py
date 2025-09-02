DIRECTIONS = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, 1),
    'v': (0, -1),
}


def loader(input_path):
    data = open(input_path, 'r').read().strip()
    return data


def unique_houses(data):
    pos = [0, 0]
    unique = set([tuple(pos)])
    for d in data:
        delta = DIRECTIONS[d]
        pos[0] += delta[0]
        pos[1] += delta[1]
        unique.add(tuple(pos))
    return unique


def solver(input_path, puzzle_type):
    assert puzzle_type in ('part1', 'part2')

    data = loader(input_path)
    
    if puzzle_type == 'part1':
        result = len(unique_houses(data))
    else:
        santa_data = data[::2]
        robo_data = data[1::2]

        santa_houses = unique_houses(santa_data)
        robo_houses = unique_houses(robo_data)

        result = len(santa_houses.union(robo_houses))

    return result


def run_examples():
    examples = (
        ('test_input', 'part1', 2),
        ('test_input', 'part2', 11),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'part1')
    part2 = solver('input', 'part2')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 2ms

    # Regression test
    assert part1 == 2565
    assert part2 == 2639


if __name__ == '__main__':
    run_examples()
    main()
