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


def get_delta(d):
    if d == '<':
        return -1,  0
    elif d == '>':
        return  1,  0
    elif d == '^':
        return  0, -1
    elif d == 'v':
        return  0,  1
    return 0, 0


def vec_add(va, vb):
    return va[0] + vb[0], va[1] + vb[1]


def reverse_moves(combination, move_dict):
    res = ''
    pos = move_dict['A']

    for c in combination:
        delta = get_delta(c)
        pos = vec_add(pos, delta)

        if pos not in move_dict.values():
            print(pos)
            raise ValueError

        if c == 'A':
            move_idx = list(move_dict.values()).index(pos)
            move = list(move_dict.keys())[move_idx]
            res += move

    return res


def check(combination):
    m = reverse_moves(combination, arrows)
    print(m)
    m = reverse_moves(m, arrows)
    print(m)
    m = reverse_moves(m, keypad)
    print(m)



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


def solve_part2(parsed_input, is_example):
    return 0


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
        ('test_input', 2, 0),
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
    print(f'Solutions found in {took:.3f}s')  # 0ms

    # Regression test
    assert part1 == 163920
    # assert part2 == 0


if __name__ == '__main__':
    run_examples()
    main()
