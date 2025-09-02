def loader(input_path):
    with open(input_path, 'r') as input_file:
        lines = input_file.read().splitlines()

    return lines


def encode_data(data):
    data = data.replace('\\', '\\\\').replace('"', '\\"')
    return '"' + data + '"'


def solver(input_path, puzzle_type):
    assert puzzle_type in ('part1', 'part2')

    raw_data = loader(input_path)
    formated_data = map(eval, raw_data)  # TODO: parse by hand?

    raw_data_sizes = map(len, raw_data)
    formated_data_sizes = map(len, formated_data)

    if puzzle_type == 'part1':
        result = sum(raw_data_sizes) - sum(formated_data_sizes)
    else:
        encoded_data = map(encode_data, raw_data)
        encoded_data_sizes = map(len, encoded_data)
        result = sum(encoded_data_sizes) - sum(raw_data_sizes)

    return result


def run_examples():
    examples = (
        ('test_input', 'part1', 12),
        ('test_input', 'part2', 19),
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
    print(f'Both solutions found in {took:.3f}s')  # 1ms

    # Regression test
    assert part1 == 1333
    assert part2 == 2046


if __name__ == '__main__':
    run_examples()
    main()
