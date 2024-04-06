import hashlib


def loader(input_path):
    data = open(input_path, 'r').read().strip()
    return data


def get_md5_with_5_zeros_number(in_hash, start):
    number = 1
    while True:
        test_hash = bytes(in_hash + str(number), 'utf-8')
        result = hashlib.md5(test_hash).hexdigest()
        if result.startswith(start):
            return number
        number += 1


def solver(input_path, puzzle_type):
    assert puzzle_type in ('part1', 'part2')

    data = loader(input_path)
    
    if puzzle_type == 'part1':
        start = '00000'
    else:
        start = '000000'

    result = get_md5_with_5_zeros_number(data, start)
    return result


def run_examples():
    examples = (
        ('test_input', 'part1', 1048970),
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
    print(f'Both solutions found in {took:.3f}s')  # 1.5s

    # Regression test
    assert part1 == 117946
    assert part2 == 3938038


if __name__ == '__main__':
    run_examples()
    main()
