
def get_unique(pairs, first):
    unique_t = set()
    for a, b in pairs:
        if a.startswith(first):
            unique_t.add(a)
        if b.startswith(first):
            unique_t.add(b)
    return unique_t


def make_connections(pairs):
    conn = {}

    for a, b in pairs:
        if a not in conn:
            conn[a] = [b]
        else:
            conn[a].append(b)

        if b not in conn:
            conn[b] = [a]
        else:
            conn[b].append(a)

    return conn


def get_loops_3(connections, starting):
    loops = set()
    
    for first in starting:
        f_conn = connections[first]
        for i, second in enumerate(f_conn):
            s_conn = connections[second]
            for third in f_conn[i + 1:]:
                if third in s_conn:
                    loop = sorted((first, second, third))
                    loops.add(tuple(loop))

    return loops


def solve_part1(pairs, is_example):
    unique_t = get_unique(pairs, 't')
    conn = make_connections(pairs)

    loops = get_loops_3(conn, unique_t)
    return len(loops)


def solve_part2(parsed_input, is_example):
    return 0


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        pairs = [l.strip().split('-') for l in puzzle.readlines()]

    return pairs


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 7),
        ('test_input', 2, 0),
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
    print(f'Solutions found in {took:.3f}s')  # 0ms

    # Regression test
    # assert part1 == 0
    # assert part2 == 0


if __name__ == '__main__':
    run_examples()
    main()
