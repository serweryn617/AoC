VOWELS = 'aeiou'
ILLEGAL = 'ab', 'cd', 'pq', 'xy'


def loader(input_path):
    for line in open(input_path, 'r'):
        yield line.strip()


def is_nice_part1(data):
    num_vowels = 0
    for c in data:
        if c in VOWELS:
            num_vowels += 1
    
    if num_vowels < 3:
        return False

    for i in ILLEGAL:
        if i in data:
            return False

    for i in range(len(data) - 1):
        if data[i] == data[i + 1]:
            return True
    
    return False


def is_nice_part2(data):
    for i in range(len(data) - 1):
        check = data[i : i + 2]
        new_data_start = data[: i]
        new_data_end = data[i + 2 :]
        if check in new_data_start or check in new_data_end:
            break
    else:
        return False

    for i in range(len(data) - 2):
        print(data[i], data[i+2])
        if data[i] == data[i + 2]:
            return True
    
    return False


def solver(input_path, puzzle_type):
    assert puzzle_type in ('part1', 'part2')

    total = 0
    for data in loader(input_path):
        if puzzle_type == 'part1':
            total += is_nice_part1(data)
        else:
            total += is_nice_part2(data)

    return total


def run_examples():
    examples = (
        ('test_input1', 'part1', 2),
        ('test_input2', 'part2', 2),
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
    print(f'Both solutions found in {took:.3f}s')  # 28ms

    # Regression test
    assert part1 == 236
    assert part2 == 51


if __name__ == '__main__':
    run_examples()
    main()
