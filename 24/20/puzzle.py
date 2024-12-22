def vec_add(va, vb):
    return va[0] + vb[0], va[1] + vb[1]


def out_of_bounds(pos, bounds):
    x, y = pos
    mx, my = bounds
    return x < 0 or x >= mx or y < 0 or y >= my


def get_char_pos(grid, char):
    for y, row in enumerate(grid):
        if char in row:
            return row.index(char), y


def grid_to_pos(grid, char):
    positions = []
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == char:
                positions.append((x, y))
    return positions


class Node:
    OPEN = 0
    CLOSED = 1

    def __init__(self, pos, cost, state, prev_pos):
        self.pos = pos
        self.cost = cost
        self.state = state
        self.prev_pos = prev_pos


class Pathfind:
    directions = (1, 0), (0, 1), (-1, 0), (0, -1)

    def __init__(self, blocked, bounds, start, end):
        self.blocked = blocked
        self.bounds = bounds

        self.start = start
        self.end = end

        self.open_nodes = [Node(start, 0, Node.OPEN, None)]
        self.closed_nodes = []

        self.cost = None
        self.last_node = None

    def open_nodes_at(self, pos):
        return [node for node in self.open_nodes if node.pos == pos]

    def closed_nodes_at(self, pos):
        return [node for node in self.closed_nodes if node.pos == pos]

    def min_cost_node_from(self, nodes):
        return min(nodes, key=lambda n: n.cost)

    def step(self):
        if not self.open_nodes:
            return True

        node = self.open_nodes.pop(0)
        node.state = Node.CLOSED
        self.closed_nodes.append(node)

        if tuple(node.pos) == tuple(self.end):
            self.cost = node.cost
            self.last_node = node
            return True

        for delta_pos in self.directions:
            next_pos = vec_add(node.pos, delta_pos)

            if out_of_bounds(next_pos, self.bounds):
                continue

            if next_pos in self.blocked:
                continue

            open_at_pos = self.open_nodes_at(next_pos)
            closed_at_pos = self.closed_nodes_at(next_pos)

            if open_at_pos or closed_at_pos:
                visited_cost = self.min_cost_node_from(open_at_pos + closed_at_pos).cost
                if node.cost > visited_cost:
                    continue

            next_cost = node.cost + 1
            self.open_nodes.append(Node(next_pos, next_cost, Node.OPEN, node.pos))

        return False

    def get_path(self):
        path = []

        node = self.last_node
        while node.prev_pos:
            path.append(node)
            node = self.min_cost_node_from(self.closed_nodes_at(node.prev_pos))
        path.append(node)

        return path


def solve_part1(grid, is_example):
    start = get_char_pos(grid, 'S')
    end = get_char_pos(grid, 'E')
    blocked = grid_to_pos(grid, '#')

    size = len(grid[0]), len(grid)

    path = Pathfind(blocked, size, start, end)
    while not path.step(): pass

    shortest = path.get_path()
    shortest = {n.pos: n.cost for n in shortest}

    shortcuts = []
    for y in range(1, size[1] - 1):
        for x in range(1, size[0] - 1):
            if (x, y) not in blocked:
                continue

            left, right = (x + 1, y), (x - 1, y)
            if left in shortest and right in shortest:
                cut_dist = abs(shortest[left] - shortest[right]) - 2
                shortcuts.append(cut_dist)

            down, up = (x, y + 1), (x, y - 1)
            if down in shortest and up in shortest:
                cut_dist = abs(shortest[down] - shortest[up]) - 2
                shortcuts.append(cut_dist)

    min_cut = 100
    if is_example:
        min_cut = 0

    return len([s for s in shortcuts if s >= min_cut])


def vec_sub(va, vb):
    return va[0] - vb[0], va[1] - vb[1]


def manhattan(va, vb):
    dx, dy = vec_sub(va, vb)
    return abs(dx) + abs(dy)


def relative_distances(shortest, min_cut, max_dist=20):
    shortest.sort(key=lambda x: x.cost)
    pairs = []

    for i in range(len(shortest) - min_cut):
        start = shortest[i]
        for j in range(i + min_cut, len(shortest)):
            end = shortest[j]

            dist = manhattan(start.pos, end.pos)
            cut_len = end.cost - start.cost - dist

            if dist <= max_dist and cut_len >= min_cut:
                pairs.append((start.pos, end.pos, cut_len))

    return pairs


def solve_part2(grid, is_example):
    start = get_char_pos(grid, 'S')
    end = get_char_pos(grid, 'E')
    blocked = grid_to_pos(grid, '#')

    bounds = len(grid[0]), len(grid)

    path = Pathfind(blocked, bounds, start, end)
    while not path.step(): pass

    shortest = path.get_path()

    min_cut = 100
    if is_example:
        min_cut = 50

    pairs = relative_distances(shortest, min_cut, max_dist=20)
    return len(pairs)


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        grid = [l.strip() for l in puzzle.readlines()]

    return grid


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 44),
        ('test_input', 2, 285),
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
    print(f'Solutions found in {took:.3f}s')  # 17042ms

    # Regression test
    assert part1 == 1518
    assert part2 == 1032257


if __name__ == '__main__':
    run_examples()
    main()
