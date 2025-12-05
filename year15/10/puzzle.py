import re
from dataclasses import dataclass


TIME = 30
ROOM = 'AA'


@dataclass
class valve_room():
    flow: int
    tunnels: list[str]


def loader(input_path):
    data = {}

    pattern = re.compile("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)")

    for line in open(input_path, 'r'):
        match = pattern.match(line)

        name = match.group(1)
        flow = int(match.group(2))
        tunnels = [t for t in match.group(3).split(", ")]

        data[name] = valve_room(flow, tunnels)

    return data


def recursive_flow(data, room, time_left):
    print(room, time_left)
    breakpoint()

    time_left -= 1

    if time_left <= 0:
        return 0

    possible_current_flow = data[room].flow * time_left
    next_rooms = data[room].tunnels

    best = 0
    for room in next_rooms:
        open_val = recursive_flow(data, room, time_left - 1) + possible_current_flow
        move_val = recursive_flow(data, room, time_left)
        best = max(best, open_val, move_val)

    # cache

    return best


def solver(input_path, puzzle_type):
    assert puzzle_type in ('part1', 'part2')

    data = loader(input_path)

    result = recursive_flow(data, ROOM, TIME)
    print(result)



def run_examples():
    examples = (
        ('test_input', 'part1', 605),
        ('test_input', 'part2', 982),
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
    print(f'Both solutions found in {took:.3f}s')

    # Regression test
    assert part1 == 1651
    # assert part2 == 909


if __name__ == '__main__':
    run_examples()
    main()
