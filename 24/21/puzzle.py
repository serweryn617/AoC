from functools import cache


def dir_first(start, end, move_dict):
    h_pos = end[0], start[1]
    v_pos = start[0], end[1]

    positions = tuple(move_dict.values())
    if v_pos in positions and h_pos in positions:
        return 'any'
    elif v_pos in positions:
        return 'v'
    return 'h'


def vertical(dy):
    if dy < 0:
        return '^' * -dy
    elif dy > 0:
        return 'v' * dy
    return ''


def horizontal(dx):
    if dx < 0:
        return '<' * -dx
    elif dx > 0:
        return '>' * dx
    return ''


def vec_sub(va, vb):
    return va[0] - vb[0], va[1] - vb[1]


keypad = {
    '7': (-2, -3), '8': (-1, -3), '9': ( 0, -3),
    '4': (-2, -2), '5': (-1, -2), '6': ( 0, -2),
    '1': (-2, -1), '2': (-1, -1), '3': ( 0, -1),
                   '0': (-1,  0), 'A': ( 0,  0),
}


arrows = {
                   '^': (-1, -1), 'A': ( 0, -1),
    '<': (-2,  0), 'v': (-1,  0), '>': ( 0,  0),
}


def add_to_all(str_list, add):
    return [s + add for s in str_list]


def all_moves(combination, move_dict):
    results = ['']
    current = move_dict['A']

    for c in combination:
        dx, dy = vec_sub(move_dict[c], current)
        first = dir_first(current, move_dict[c], move_dict)
        current = move_dict[c]

        if first == 'any' and dx and dy:
            v_first_results = add_to_all(results, vertical(dy) + horizontal(dx) + 'A')
            h_first_results = add_to_all(results, horizontal(dx) + vertical(dy) + 'A')
            results = v_first_results + h_first_results
        else:
            if first == 'h':
                results = add_to_all(results, horizontal(dx) + vertical(dy) + 'A')
            else:
                results = add_to_all(results, vertical(dy) + horizontal(dx) + 'A')

    return results


def solve_part1(combinations, is_example):
    total = 0

    for combination in combinations:
        comb_min = None
        keypad_possible = all_moves(combination, keypad)

        for kp in keypad_possible:
            arrow1_possible = all_moves(kp, arrows)

            for ap in arrow1_possible:
                arrow2_possible = all_moves(ap, arrows)
                curr_min = min(map(len, arrow2_possible))

                if comb_min is None:
                    comb_min = curr_min
                else:
                    comb_min = min(comb_min, curr_min)

        total += comb_min * int(combination[:-1])

    return total


def make_combination(data, add):
    result = []

    for a in add:
        result.extend(add_to_all(data, a))

    return result


def get_arrow_directions(start, end):
    start_pos = arrows[start]
    end_pos = arrows[end]

    dx, dy = vec_sub(end_pos, start_pos)
    first = dir_first(start_pos, end_pos, arrows)

    h = horizontal(dx)
    v = vertical(dy)

    if first == 'v':
        return v + h + 'A',
    elif first == 'h':
        return h + v + 'A',

    return v + h + 'A', h + v + 'A'


keys = ('^', '<', 'v', '>', 'A')
lut = {s: {e: get_arrow_directions(s, e) for e in keys} for s in keys}


def substitute_moves(combination):
    res = ['']
    start = 'A'

    for i in range(len(combination)):
        if i > 0:
            start = combination[i - 1]
        end = combination[i]
        res = make_combination(res, lut[start][end])

    return res


@cache
def recursive_length(levels, pattern):
    if levels == 0:
        return len(pattern)

    assert pattern[-1] == 'A'
    patterns = substitute_moves(pattern)

    min_len = None

    for pattern in patterns:
        length = 0
        parts = [m + 'A' for m in pattern.split('A')]

        if parts[-1] == 'A':
            parts.pop(-1)

        for p in parts:
            length += recursive_length(levels - 1, p)

        min_len = min(min_len, length) if min_len is not None else length

    return min_len


def solve_part2(combinations, is_example):
    total = 0

    for combination in combinations:
        keypad_moves = all_moves(combination, keypad)

        min_len = None

        for kp in keypad_moves:
            l = recursive_length(25, kp)

            if min_len is None:
                min_len = l
            else:
                min_len = min(min_len, l)

        total += min_len * int(combination[:-1])

    return total


def loader(input_path):
    nums = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            line = line.strip()
            assert line[-1] == 'A'
            nums.append(line)

    return nums


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 126384),
        ('test_input', 2, 154115708116294),
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
    print(f'Solutions found in {took:.3f}s')  # 62ms

    # Regression test
    assert part1 == 163920
    assert part2 == 204040805018350


if __name__ == '__main__':
    run_examples()
    main()
