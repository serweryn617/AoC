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

    # In the first part of the puzzle iterate over numbers and check if they have symbols adjacent
    # This will give correct result if a number has more than one symbol around it
    for pos, c in enumerate(lines[1]):
        if c.isdigit():
            num_string += c
            if first is None:
                first = pos
            last = max(pos, last)
        elif num_string:  # reached the end of number
            adjacent = get_adjacent_symbols(lines, first, last)
            if adjacent != '':
                line_count += int(num_string)
            elif adjacent == '*':
                pass
            num_string = ''
            first = None

    return line_count


def get_adjacent_gear(lines: list, first: int, last: int):
    symbols = ''

    if last < len(lines[1]) - 1:
        last += 2
        if lines[1][last - 1] == '*':
            return last - 1, 0
    if first > 0:
        first -= 1
        if lines[1][first] == '*':
            return first, 0

    idx = lines[0][first:last].find('*')
    if idx >= 0:
        return first + idx, -1

    idx = lines[2][first:last].find('*')
    if idx >= 0:
        return first + idx, 1


gears = {}
'''Sparse gear array'''


def count_gears(lines: list, line_num: int):
    num_string = ''
    first = None
    last = 0

    for pos, c in enumerate(lines[1]):
        if c.isdigit():
            num_string += c
            if first is None:
                first = pos
            last = max(pos, last)
        elif num_string:  # reached the end of number
            adjacent = get_adjacent_symbols(lines, first, last)
            if adjacent == '*':
                x, y = get_adjacent_gear(lines, first, last)
                key = f'{x},{line_num + y}'
                if key in gears:
                    gears[key].append(int(num_string))
                else:
                    gears[key] = [int(num_string)]
            num_string = ''
            first = None


def sum_gear_ratios():
    total = 0

    for pairs in gears.values():
        if len(pairs) != 2:
            continue

        total += pairs[0] * pairs[1]

    return total


def solver(input_path, puzzle_type: str):
    assert puzzle_type in ('sum', 'ratio')

    puzzle_answer = 0

    with open(input_path, 'r') as puzzle:
        lines = [
            '',
            puzzle.readline(),  # Leave new lines at the end
            puzzle.readline(),
        ]
        line_num = 0

        while lines[1] != '':
            if puzzle_type == 'sum':
                puzzle_answer += count_part_numbers(lines)
            else:
                count_gears(lines, line_num)

            lines[0], lines[1], lines[2] = lines[1], lines[2], puzzle.readline()
            line_num += 1

    if puzzle_type == 'ratio':
        puzzle_answer = sum_gear_ratios()

    return puzzle_answer


if __name__ == '__main__':
    expected1 = 4361
    result1 = solver('test_input', 'sum')
    assert result1 == expected1, f'Example 1 failed: {result1}'

    expected2 = 467835
    result2 = solver('test_input', 'ratio')
    assert result2 == expected2, f'Example 2 failed: {result2}'

    part1 = solver('input', 'sum')
    part2 = solver('input', 'ratio')

    print("Examples passed")
    print("Puzzle 1 answer:", part1)
    print("Puzzle 2 answer:", part2)

    # Regression test
    assert part1 == 54388
    assert part2 == 80253814

