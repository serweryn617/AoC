GEAR = '*'


def get_adjacent_symbols(lines: list, first: int, last: int):
    symbols = ''

    if last < len(lines[1]) - 1:
        last += 2
        symbols += lines[1][last - 1]
    if first > 0:
        first -= 1
        symbols += lines[1][first]

    symbols += lines[0][first:last] + lines[2][first:last]

    return symbols.replace('.', '').strip()


def count_part_numbers(lines: list):
    num_string = ''
    line_count = 0
    first = None
    last = 0
    end_pos = len(lines[1]) - 1

    # In the first part of the puzzle iterate over numbers and check if they have symbols adjacent
    # This will give correct result if a number has more than one symbol around it
    for pos, c in enumerate(lines[1]):
        if c.isdigit():
            num_string += c
            if first is None:
                first = pos
            last = pos
        if num_string and (not c.isdigit() or pos == end_pos):  # reached the end of number or line
            adjacent = get_adjacent_symbols(lines, first, last)
            if adjacent != '':
                line_count += int(num_string)
            num_string = ''
            first = None

    return line_count


def get_adjacent_gear(lines: list, first: int, last: int):
    if first > 0:
        first -= 1
        if lines[1][first] == GEAR:
            return first, 0

    if last < len(lines[1]) - 1:
        last += 1
        if lines[1][last] == GEAR:
            return last, 0

    idx = lines[0][first:last + 1].find(GEAR)
    if idx >= 0:
        return first + idx, -1

    idx = lines[2][first:last + 1].find(GEAR)
    if idx >= 0:
        return first + idx, 1


# TODO: Code duplicate
def count_gears(lines: list, line_num: int, gears: dict):
    num_string = ''
    first = None
    last = 0
    end_pos = len(lines[1]) - 1

    for pos, c in enumerate(lines[1]):
        if c.isdigit():
            num_string += c
            if first is None:
                first = pos
            last = pos
        if num_string and (not c.isdigit() or pos == end_pos):  # reached the end of number
            adjacent = get_adjacent_symbols(lines, first, last)
            if adjacent == GEAR:
                x, dy = get_adjacent_gear(lines, first, last)
                key = x, line_num + dy
                if key in gears:
                    gears[key].append(int(num_string))
                else:
                    gears[key] = [int(num_string)]
            num_string = ''
            first = None


def sum_gear_ratios(gears):
    total = 0

    for pairs in gears.values():
        if len(pairs) != 2:
            continue

        total += pairs[0] * pairs[1]

    return total


def solver(input_path, puzzle_type: str):
    assert puzzle_type in ('sum', 'ratio')

    puzzle_answer = 0
    gears = {}
    '''Sparse gear array'''

    with open(input_path, 'r') as puzzle:
        lines = [
            '',
            puzzle.readline().rstrip(),
            puzzle.readline().rstrip(),
        ]
        line_num = 0

        while lines[1] != '':
            if puzzle_type == 'sum':
                puzzle_answer += count_part_numbers(lines)
            else:
                count_gears(lines, line_num, gears)
                line_num += 1

            lines[0], lines[1], lines[2] = lines[1], lines[2], puzzle.readline().rstrip()

    if puzzle_type == 'ratio':
        puzzle_answer = sum_gear_ratios(gears)

    return puzzle_answer


def run_examples():
    examples = (
        ('test_input', 'sum', 4361),
        ('test_input', 'ratio', 467835),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {puzzle_type} {path} failed: {result}'

    print('Examples passed')


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'sum')
    part2 = solver('input', 'ratio')

    took = time.time() - start_time

    print("Puzzle 1 answer:", part1)
    print("Puzzle 2 answer:", part2)
    print(f'Both solutions found in {took:.3f}s')  # 3ms

    # Regression test
    assert part1 == 530495
    assert part2 == 80253814


if __name__ == '__main__':
    run_examples()
    main()
