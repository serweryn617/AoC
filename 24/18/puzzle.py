def vec_add(va, vb):
    return va[0] + vb[0], va[1] + vb[1]


def out_of_bounds(pos, max_x, max_y):
    x, y = pos
    return x < 0 or x >= max_x or y < 0 or y >= max_y


class pathfind:
    OPEN = 0
    CLOSED = 1

    directions = (1, 0), (0, 1), (-1, 0), (0, -1)

    def __init__(self, blocked, size, start, end):
        self.blocked = blocked
        self.max_x = size
        self.max_y = size

        self.start = start
        self.end = end

        self.nodes = {(*start, 0): (self.OPEN, )}
        self.cost = None

    def get_nodes_at(self, x, y):
        nodes = {k: v for k, v in self.nodes.items() if k[0] == x and k[1] == y}
        return nodes

    def get_min_cost_at(self, x, y):
        nodes = self.get_nodes_at(x, y)
        if not nodes:
            return
        node, _ = min(nodes.items(), key=lambda i: i[0][2])
        _, _, cost = node
        return cost

    def step(self):
        open_nodes = {k: v for k, v in self.nodes.items() if v[0] == self.OPEN}
        if not open_nodes:
            return True

        node, _ = min(open_nodes.items(), key=lambda i: i[0][2])
        *node_pos, cost = node
        self.nodes[node] = (self.CLOSED,)

        if tuple(node_pos) == tuple(self.end):
            self.cost = cost
            return True

        for delta_pos in self.directions:
            next_pos = vec_add(node_pos, delta_pos)

            if out_of_bounds(next_pos, self.max_x, self.max_y):
                continue

            if next_pos in self.blocked:
                continue

            if self.get_nodes_at(*next_pos):
                visited_cost = self.get_min_cost_at(*next_pos)
                if cost > visited_cost:
                    continue

            next_cost = cost + 1
            key = (*next_pos, next_cost)
            if key not in self.nodes:
                self.nodes[key] = (self.OPEN,)

        return False


def solve_part1(blocked, is_example):
    size = 70
    num = 1024

    if is_example:
        size = 6
        num = 12

    start = 0, 0
    end = size, size

    path = pathfind(blocked[:num], size + 1, start, end)
    while not path.step(): pass
    cost = path.cost

    return cost


def flood(size, blocked, pos, end, visited=None):
    visited = visited or []

    if pos == end:
        return True

    if pos in blocked or pos in visited or out_of_bounds(pos, size, size):
        return False

    visited.append(pos)

    directions = (1, 0), (0, 1), (-1, 0), (0, -1)
    for delta in directions:
        next_pos = vec_add(pos, delta)
        ok = flood(size, blocked, next_pos, end, visited)
        if ok:
            return True

    return False


def solve_part2(blocked, is_example):
    size = 70
    num = 1024

    if is_example:
        size = 6
        num = 12

    start = 0, 0
    end = size, size

    for i in range(num, len(blocked)):
        ok = flood(size + 1, blocked[:i], start, end)
        if not ok: break

    corrupt = blocked[i - 1]
    return ','.join(map(str, corrupt))


def loader(input_path):
    data = []
    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            x, y = line.strip().split(',')
            data.append((int(x), int(y)))
    return data


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 22),
        ('test_input', 2, '6,1'),
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
    print(f'Solutions found in {took:.3f}s')  # 32585ms

    # Regression test
    assert part1 == 232
    assert part2 == '44,64'


if __name__ == '__main__':
    run_examples()
    main()
