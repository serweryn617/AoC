import itertools
from math import ceil


def loader(input_path):
    data = []

    for line in open(input_path, 'r'):
        start, _, end, _, distance = line.split()
        data.append((start, end, int(distance)))

    return data


def unique_destinations(data):
    unique = set()

    for start, end, _ in data:
        unique.add(start)
        unique.add(end)

    return list(unique)


def solver(input_path, puzzle_type):
    assert puzzle_type in ('part1', 'part2')

    data = loader(input_path)
    unique = unique_destinations(data)

    distance_table = dict.fromkeys(unique)
    for start, end, distance in data:
        if distance_table[start] is None:
            distance_table[start] = dict.fromkeys(unique)
        distance_table[start][end] = distance
        
        if distance_table[end] is None:
            distance_table[end] = dict.fromkeys(unique)
        distance_table[end][start] = distance

    range_unique = range(len(unique))
    permutations = sorted(itertools.permutations(range_unique))

    # reduce time by half
    reduced_len = ceil(len(permutations) / 2)
    permutations = permutations[:reduced_len]

    if puzzle_type == 'part1':
        comparator = min
    else:
        comparator = max

    # brute force, there's only 8 nodes
    result = None
    for perm in permutations:
        distance = 0
        for i in range(len(perm) - 1):
            start, end = unique[perm[i]], unique[perm[i + 1]]
            distance += distance_table[start][end]

        if result is None:
            result = distance
        else:
            result = comparator(result, distance)

    return result


def run_examples():
    examples = (
        ('test_input', 'part1', 605),
        ('test_input', 'part2', 982),
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
    print(f'Both solutions found in {took:.3f}s')  # 35ms

    # Regression test
    assert part1 == 117
    assert part2 == 909


if __name__ == '__main__':
    run_examples()
    main()
