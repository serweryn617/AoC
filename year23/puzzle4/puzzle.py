def solver(input_path, puzzle_type: str):
    assert puzzle_type in ('sum', 'copies')

    puzzle_answer = 0

    with open(input_path, 'r') as puzzle:
        lines = puzzle.readlines()
        
        if puzzle_type == 'copies':
            copy_number = [1 for _ in lines]

        for num, line in enumerate(lines):
            _, line = line.split(':')
            numbers, winning = line.split('|')
            numbers = numbers.split()
            winning = winning.split()

            num_wins = len(numbers + winning) - len(set(numbers + winning))

            if puzzle_type == 'copies':
                for i in range(num + 1, num + num_wins + 1):
                    copy_number[i] += copy_number[num]
            else:
                puzzle_answer += num_wins and 2 ** (num_wins - 1)

    if puzzle_type == 'copies':
        return sum(copy_number)
    else:
        return puzzle_answer


def run_examples():
    examples = (
        ('test_input', 'sum', 13),
        ('test_input', 'copies', 30),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} failed: {result}'

    print('Examples passed')


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'sum')
    part2 = solver('input', 'copies')

    took = time.time() - start_time

    print("Examples passed")
    print("Puzzle 1 answer:", part1)
    print("Puzzle 2 answer:", part2)
    print(f'Both solutions found in {took:.3f}s')  # 1ms

    # Regression test
    assert part1 == 21213
    assert part2 == 8549735


if __name__ == '__main__':
    run_examples()
    main()



