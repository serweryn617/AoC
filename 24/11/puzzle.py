from functools import cache


def make_stone_dict(stones):
    d = {}
    for s in stones:
        if s not in d:
            d[s] = 1
        else:
            d[s] += 1
    return d


def add_to_stone_dict(stones, add_list, count):
    for key in add_list:
        if key not in stones:
            stones[key] = count
        else:
            stones[key] += count


@cache
def blink_single(s):
    if s == 0:
        return [1]

    num_digits = len(str(s))
    if num_digits % 2 == 0:
        half = num_digits // 2
        a = int(str(s)[:half])
        b = int(str(s)[half:])
        return [a, b]
    else:
        return [s * 2024]


def blink(stones, num):
    for _ in range(num):
        next_stones = {}
        for s, c in stones.items():
            add = blink_single(s)
            add_to_stone_dict(next_stones, add, c)

        stones = next_stones

    return stones


def solve_part1(stones):
    new = blink(stones, 25)
    return sum(new.values())


def solve_part2(stones):
    new = blink(stones, 75)
    return sum(new.values())


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        stones = [int(s) for s in puzzle.readline().split()]

    return make_stone_dict(stones)


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 55312),
        ('test_input', 2, 65601038650482),
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
    print(f'Solutions found in {took:.3f}s')  # 24ms

    # Regression test
    assert part1 == 203953
    assert part2 == 242090118578155


if __name__ == '__main__':
    run_examples()
    main()
