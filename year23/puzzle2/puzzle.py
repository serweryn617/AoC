CUBES = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def calculate_game_data(turns):
    max_cubes = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }

    for turn_string in turns:
        turn = turn_string.replace(',', '').split()
        for color in CUBES:
            if color not in turn:
                continue
            index = turn.index(color) - 1
            max_cubes[color] = max(int(turn[index]), max_cubes[color])

    possible = (max_cubes['red'] <= CUBES['red'] and
                max_cubes['green'] <= CUBES['green'] and
                max_cubes['blue'] <= CUBES['blue'])
    power = max_cubes['red'] * max_cubes['green'] * max_cubes['blue']
    return possible, power


def process_game(game):
    game_id_string, turns_string = game.split(':')
    game_id = int(game_id_string.split()[1])
    turns = turns_string.split(';')

    game_possible, game_power = calculate_game_data(turns)

    return game_id if game_possible else 0, game_power


def solver(input_path):
    possible = 0
    power = 0

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            game_id, game_power = process_game(line)

            possible += game_id
            power += game_power

    return possible, power


def run_examples():
    examples = (
        ('test_input', 0, 8),
        ('test_input', 1, 2286),
    )

    for path, part, expected in examples:
        result = solver(path)[part]
        assert result == expected, f'Example {path} failed: {result}'

    print('Examples passed')


def main():
    import time
    start_time = time.time()

    part1, part2 = solver('input')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)  # 2006
    print('Puzzle 2 answer:', part2)  # 84911
    print(f'Both solutions found in {took:.3f}s')  # <1ms

    # Regression test
    assert part1 == 2006
    assert part2 == 84911


if __name__ == '__main__':
    run_examples()
    main()
