import itertools
from operator import xor


def calc_num_button_presses(light, button_masks):
    for i in range(1, len(button_masks) + 1):
        for comb in itertools.combinations(button_masks, r=i):
            mask = tuple(itertools.accumulate(comb, xor, initial=0))[-1]
            if mask == light:
                return i
    raise RuntimeError(f"Combination not found for light {light}, button_masks {button_masks}")


def solve_part1(parsed_input):
    total = 0
    for light, button_masks, _, _ in parsed_input:
        total += calc_num_button_presses(light, button_masks)
    return total


def compare(current, target):
    res = 0
    for c, t in zip(current, target, strict=True):
        if c > t:
            return -1
        if c < t:
            res = 1
    return res


def piecewise_add(target, button, mult=1):
    target = list(target)
    for i in button:
        target[i] += mult
    return tuple(target)


def max_diff(current, target, button):
    val = []
    for i in button:
        val.append(target[i] - current[i])
    return min(val)


def search_num_presses(buttons, current, target, num_presses=0):
    comp = compare(current, target)
    if comp == 0:
        return num_presses
    elif comp == -1:
        return 0

    if len(buttons) == 0:
        return 0

    max_range = max_diff(current, target, buttons[0])

    for i in range(max_range, -1, -1):
        curr = piecewise_add(current, buttons[0], mult=i)
        s = search_num_presses(buttons[1:], curr, target, num_presses + i)
        if s > 0:
            return s
    return 0


def solve_part2(parsed_input):
    total = 0
    i = 1
    for _, _, button_tuples, joltage in parsed_input:
        # Pressing buttons that update multiple counters at once is fastest, then do a DFS
        button_tuples.sort(key=lambda x: len(x), reverse=True)
        empty = tuple([0 for _ in joltage])
        total += search_num_presses(tuple(button_tuples), empty, joltage)
    return total


def get_light_mask(lights):
    lights = lights.strip("[]")
    res = 0
    for i, state in enumerate(lights):
        if state == '#':
            res |= (1 << i)
    return res


def get_button_masks(buttons):
    masks = []
    for button in buttons:
        str_arr = button.strip("()").split(',')
        arr = map(int, str_arr)
        res = 0
        for i in arr:
            res |=  (1 << i)
        masks.append(res)
    return masks


def get_button_tuples(buttons):
    tuples = []
    for button in buttons:
        str_arr = button.strip("()").split(',')
        arr = map(int, str_arr)
        tuples.append(tuple(arr))
    return tuples


def get_joltage_tuple(joltage):
    str_arr = joltage.strip("{}").split(',')
    arr = map(int, str_arr)
    return tuple(arr)


def loader(input_path):
    data = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle:
            light, *buttons, joltage = line.split()

            light = get_light_mask(light)
            button_masks = get_button_masks(buttons)
            button_tuples = get_button_tuples(buttons)
            joltage_tuple = get_joltage_tuple(joltage)

            data.append((light, button_masks, button_tuples, joltage_tuple))

    return data


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 7),
        ('test_input', 2, 33),
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
    print(f'Solutions found in {took:.3f}s')  # xms

    # Regression test
    assert part1 == 428
    # assert part2 == 0


if __name__ == '__main__':
    # run_examples()
    main()
