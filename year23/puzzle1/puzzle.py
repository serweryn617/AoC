DIGITS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}
COMPARE_LENGTH = max(map(len, DIGITS))


def is_word_at(line, pos):
    for word in DIGITS:
        if line.startswith(word, pos, pos + COMPARE_LENGTH):
            return DIGITS[word]
    return None


def update(values_list: list, value: str):
    if values_list[0] is None:
        values_list[0] = value
    values_list[1] = value


def process_line(line: str, include_words: bool):
    values = [None, None]

    for pos, c in enumerate(line):
        if c.isdigit():
            update(values, c)
        elif include_words:
            value = is_word_at(line, pos)
            if value is not None:
                update(values, value)

    return int(values[0] + values[1])


def solver(path: str, include_words: bool = False):
    puzzle_answer = 0

    with open(path, 'r') as puzzle:
        for line in puzzle.readlines():
            puzzle_answer += process_line(line, include_words)

    return puzzle_answer


def run_examples():
    examples = (
        ('test_input1', False, 142),
        ('test_input2', True, 281),
    )

    for path, include_words, expected in examples:
        result = solver(path, include_words)
        assert result == expected, f'Example {path} failed: {result}'

    print('Examples passed')


def main():
    import time
    start_time = time.time()

    part1 = solver('input', False)
    part2 = solver('input', True)
    
    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)  # 54388
    print('Puzzle 2 answer:', part2)  # 53515
    print(f'Both solutions found in {took:.3f}s')  # 12ms

    # Regression test
    assert part1 == 54388
    assert part2 == 53515


if __name__ == '__main__':
    run_examples()
    main()
