def vec_add(va, vb):
    return va[0] + vb[0], va[1] + vb[1]


def out_of_bounds(pos, max_x, max_y):
    x, y = pos
    return x < 0 or x >= max_x or y < 0 or y >= max_y


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


class pathfind:
    OPEN = 0
    CLOSED = 1

    directions = (1, 0), (0, 1), (-1, 0), (0, -1)

    def __init__(self, blocked, size, start, end):
        self.blocked = blocked
        self.max_x = size[0]
        self.max_y = size[1]

        self.start = start
        self.end = end

        self.nodes = {(*start, 0): (self.OPEN, None)}
        self.cost = None
        self.last_node = None

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

        node, data = min(open_nodes.items(), key=lambda i: i[0][2])
        *node_pos, cost = node
        _, parent = data
        self.nodes[node] = (self.CLOSED, parent)

        if tuple(node_pos) == tuple(self.end):
            self.cost = cost
            self.last_node = node
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
                self.nodes[key] = (self.OPEN, node)

        return False

    def get_path(self):
        path = []

        node = self.last_node
        while node:
            path.append(node)
            node = self.nodes[node][1]

        return path



def solve_part1(grid, is_example):
    start = get_char_pos(grid, 'S')
    end = get_char_pos(grid, 'E')
    blocked = grid_to_pos(grid, '#')

    size = len(grid[0]), len(grid)

    path = pathfind(blocked, size, start, end)
    while not path.step(): pass

    shortest = path.get_path()
    shortest = {(x, y): c for x, y, c in shortest}

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


def solve_part2(parsed_input, is_example):
    return 0


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
    assert part1 == 1518
    # assert part2 == 0


if __name__ == '__main__':
    run_examples()
    main()
