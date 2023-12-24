STEPS = (-3, -2, -1, 1, 2, 3)


class Head:
    def __init__(self, position, length = 0, visited = ()):
        self.pos = position
        self.length = length
        self.visited = visited

    def sort_key(self):
        return self.length


def step(head, grid, size = 3):
    x, y, step_vertical = head.pos

    x_min, x_max = 0, len(grid[0]) - 1
    y_min, y_max = 0, len(grid) - 1

    next_heads = []

    if step_vertical:
        for delta in range(-size, size + 1):
            if delta == 0 or not y_min <= y + delta <= y_max:
                continue

            visited = list((x, vy) for vy in range(min(y, y + delta), max(y, y + delta) + 1))
            visited.pop(visited.index((x, y)))
            weight = sum([grid[vy][vx] for vx, vy in visited])

            new_head = Head((x, y + delta, not step_vertical), head.length + weight, head.visited + tuple(visited))
            next_heads.append(new_head)
    else:  # step horizontal
        for delta in range(-size, size + 1):
            if delta == 0 or not x_min <= x + delta <= x_max:
                continue

            visited = list((vx, y) for vx in range(min(x, x + delta), max(x, x + delta) + 1))
            visited.pop(visited.index((x, y)))
            weight = sum([grid[vy][vx] for vx, vy in visited])

            new_head = Head((x + delta, y, not step_vertical), head.length + weight, head.visited + tuple(visited))
            next_heads.append(new_head)

    # print(f'Next for {head.pos}: {head.length}')
    # for h in next_heads:
    #     print(h.pos, h.length)

    return next_heads


def display_visited(visited):
    print('Visited:')
    for v in visited:
        print(v, end=' ')
    print()

    print('Graph:')
    for y in range(13):
        for x in range(13):
            if (x, y) in visited:
                print('X', end='')
            else:
                print('.', end='')
        print()


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        grid = [line.strip() for line in puzzle.readlines()]

    for i in range(len(grid)):
        grid[i] = [int(tile) for tile in grid[i]]

    return grid


def solver(input_path, puzzle_type):
    # assert puzzle_type in ('energized', 'max')

    grid = loader(input_path)

    # Z true - next step vertical
    heads = [
        Head((0, 0, True), visited=((0,0),)),
        Head((0, 0, False), visited=((0,0),)),
    ]
    # heads = [
    #     Head((1, 0, True), grid[0][1], ((0, 0), (1, 0))),
    #     Head((2, 0, True), grid[0][1] + grid[0][2], ((0, 0), (1, 0), (2, 0))),
    #     Head((0, 1, False), grid[1][0], ((0, 0), (0, 1))),
    #     Head((0, 2, False), grid[1][0] + grid[2][0], ((0, 0), (0, 1), (0, 2))),
    # ]
    end = len(grid[0]) - 1, len(grid) - 1

    while True:
        # head = min(heads, key=Head.sort_key)
        heads.sort(key=Head.sort_key)
        head = heads[0]

        # print('selecting', heads[0].pos, heads[0].length)

        if head.pos[:2] == end:
            print('end', head.length)
            display_visited(head.visited)
            return head.length
            break

        new_heads = step(head, grid)
        heads_pos = [h.pos for h in heads]

        for new in new_heads:
            if new.pos not in heads_pos:
                # print('appending', new.pos, new.length)
                heads.append(new)
            else:
                idx = heads_pos.index(new.pos)
                if new.length < heads[idx].length:
                    heads.pop(idx)
                    heads.append(new)

        heads.pop(heads.index(head))

        print('m', min(h.length for h in heads), len(heads))
        # print('m', len(set(h.pos for h in heads)), len(heads))

    # for h in heads:
    #     print('Pos list', h.pos)

    return min_heat_loss


def run_examples():
    examples = (
        ('test_input', 'heat', 102),
        # ('test_input', 'max', 51),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'energized')
    # part2 = solver('input', 'max')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    # print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 735ms

    # Regression test
    # assert part1 == 
    # assert part2 == 


if __name__ == '__main__':
    run_examples()
    main()

    # import cProfile
    # cProfile.run("solver('test_input', 1)")
