def loader(input_path):
    data = open(input_path, 'r').read()

    return data


def part2_solver(data):
    level = 0
    for num, char in enumerate(data):
        if char == '(':
            level += 1
        elif char == ')':
            level -= 1
        if level < 0:
            return num + 1


def solver(input_path, puzzle_type):
    assert puzzle_type in ('end', 'first')

    data = loader(input_path)
    
    if puzzle_type == 'end':
        up = data.count('(')
        down = data.count(')')
        result = up - down
    else:
        result = part2_solver(data)

    return result


def run_examples():
    examples = (
        ('test_input1', 'end', -3),
        ('test_input2', 'first', 5),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'end')
    part2 = solver('input', 'first')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # <1ms

    # Regression test
    assert part1 == 74
    assert part2 == 1795


if __name__ == '__main__':
    run_examples()
    main()
