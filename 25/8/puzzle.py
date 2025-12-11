import itertools
import math


def distance3(a, b):
    ax, ay, az = a
    bx, by, bz = b

    dx, dy, dz = ax - bx, ay - by, az - bz

    return dx**2 + dy**2 + dz**2


def add_connection(circuits, idx_a, idx_b):
    added_to = []

    for i, circuit in enumerate(circuits):
        if idx_a in circuit and idx_b in circuit:
            return 0
        if idx_a in circuit or idx_b in circuit:
            circuit.add(idx_a)
            circuit.add(idx_b)
            added_to.append(i)

    if added_to:
        base = circuits[added_to[0]]
        for i in reversed(added_to[1:]):
            base.update(circuits.pop(i))
        return 1

    circuits.append(set((idx_a, idx_b)))
    return 1


def solve_part1(lights, is_example):
    distances = []
    idx_combs = itertools.combinations(range(len(lights)), r=2)

    for a, b in idx_combs:
        distances.append((distance3(lights[a], lights[b]), a, b))
    distances.sort()

    circuits = []
    num_conns = 0
    for d, idx_a, idx_b in distances:
        add_connection(circuits, idx_a, idx_b)
        num_conns += 1
        if num_conns == (10 if is_example else 1000):
            break

    sizes = [len(c) for c in circuits]
    max_sizes = sorted(sizes, reverse=True)[:3]

    return math.prod(max_sizes)


def solve_part2(lights, is_example):
    distances = []
    idx_combs = itertools.combinations(range(len(lights)), r=2)

    for a, b in idx_combs:
        distances.append((distance3(lights[a], lights[b]), a, b))
    distances.sort()

    circuits = []
    num_conns = 0
    for d, idx_a, idx_b in distances:
        add_connection(circuits, idx_a, idx_b)
        if len(circuits) == 1 and len(circuits[0]) == len(lights):
            x1, x2 = lights[idx_a][0], lights[idx_b][0]
            break

    return x1 * x2


def loader(input_path):
    data = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle:
            coords = line.strip().split(",")
            data.append([int(c) for c in coords])

    return data


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 40),
        ('test_input', 2, 25272),
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
    print(f'Solutions found in {took:.3f}s')  # 850ms

    # Regression test
    assert part1 == 244188
    assert part2 == 8361881885


if __name__ == '__main__':
    run_examples()
    main()
