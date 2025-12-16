import functools


END = "out"


def get_num_connections(devices):

    @functools.cache
    def get_connection(current_device):
        if current_device == END:
            return 1

        nonlocal devices
        connections = devices[current_device]
        num_conns = 0
        for c in connections:
            num_conns += get_connection(c)
        return num_conns

    START = "you"
    return get_connection(START)


def solve_part1(parsed_input):
    return get_num_connections(parsed_input)


def get_num_connections_through_specific_nodes(devices):

    @functools.cache
    def get_connection(current_device, visited_dac=False, visited_fft=False):
        if current_device == END:
            return 1 if visited_dac and visited_fft else 0

        nonlocal devices
        connections = devices[current_device]
        num_conns = 0
        for c in connections:
            next_dac = (c == "dac")
            next_fft = (c == "fft")
            num_conns += get_connection(c, visited_dac or next_dac, visited_fft or next_fft)
        return num_conns

    START = "svr"
    return get_connection(START)


def solve_part2(parsed_input):
    return get_num_connections_through_specific_nodes(parsed_input)


def loader(input_path):
    data = {}

    with open(input_path, 'r') as puzzle:
        for line in puzzle:
            device, *connections = line.split()
            device = device.strip(":")
            data[device] = connections

    return data


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 5),
        ('test_input_2', 2, 2),
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
    print(f'Solutions found in {took:.3f}s')  # 1ms

    # Regression test
    assert part1 == 772
    assert part2 == 423227545768872


if __name__ == '__main__':
    run_examples()
    main()
