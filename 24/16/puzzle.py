def vec_add(va, vb):
    return va[0] + vb[0], va[1] + vb[1]


def out_of_bounds(pos, max_x, max_y):
    x, y = pos
    return x < 0 or x >= max_x or y < 0 or y >= max_y


def get_char_pos(grid, char):
    for y, row in enumerate(grid):
        if char in row:
            return row.index(char), y


def get_dir_change_cost(curr_dir, next_dir):
    if curr_dir == next_dir:
        return 0

    if (curr_dir == '<' or curr_dir == '>') and (next_dir == '<' or next_dir == '>'):
        return 2000

    if (curr_dir == '^' or curr_dir == 'v') and (next_dir == '^' or next_dir == 'v'):
        return 2000

    return 1000


class path:
    OPEN = 0
    CLOSED = 1
    WALL = '#'

    directions = {
        '>': (1, 0),
        'v': (0, 1),
        '<': (-1, 0),
        '^': (0, -1),
    }

    def __init__(self, grid, start, end):
        self.grid = grid
        self.max_x = len(grid[0])
        self.max_y = len(grid)

        self.start = start
        self.end = end

        self.nodes = {(*start, '>', 0): (self.OPEN, 0, None)}
        self.last_nodes = []
        self.total_cost = None

    def get_nodes_at(self, x, y, d):
        nodes = {k: v for k, v in self.nodes.items() if k[0] == x and k[1] == y and k[2] == d}
        return nodes

    def get_min_cost_at(self, x, y, d):
        nodes = self.get_nodes_at(x, y, d)
        if not nodes:
            return
        node, _ = min(nodes.items(), key=lambda i: i[0][3])
        _, _, _, cost = node
        return cost

    def step(self):
        open_nodes = {k: v for k, v in self.nodes.items() if v[0] == self.OPEN}
        if not open_nodes:
            return True

        node, value = min(open_nodes.items(), key=lambda i: i[0][3])

        *node_pos, node_dir, cost = node
        _, num, parents = value

        self.nodes[node] = self.CLOSED, num, parents

        if self.total_cost is not None and cost > self.total_cost:
            return False

        if tuple(node_pos) == tuple(self.end):
            self.last_nodes.append(node)
            self.total_cost = cost
            return False

        for next_dir, delta_pos in self.directions.items():
            next_pos = vec_add(node_pos, delta_pos)

            if out_of_bounds(next_pos, self.max_x, self.max_y):
                continue

            if self.grid[next_pos[1]][next_pos[0]] == self.WALL:
                continue

            if self.get_nodes_at(*next_pos, next_dir):
                visited_cost = self.get_min_cost_at(*next_pos, next_dir)
                if cost > visited_cost:
                    continue

            next_cost = cost + get_dir_change_cost(node_dir, next_dir) + 1
            key = (*next_pos, next_dir, next_cost)
            if key in self.nodes:
                self.nodes[key][2].append(node)
            else:
                self.nodes[key] = self.OPEN, num + 1, [node]

        return False

    def populate_parents(self, parent_list, node):
        parents = self.nodes[node][2]
        if parents is None:
            return
        for p in parents:
            parent_list.append(p[:2])
            self.populate_parents(parent_list, p)

    def winning_nodes(self):
        parent_list = []
        for node in self.last_nodes:
            parent_list.append(node[:2])
            self.populate_parents(parent_list, node)
        return parent_list

    def num_winning_nodes(self):
        nodes = self.winning_nodes()
        return len(set(nodes))


def show(grid, nodes):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            c = grid[y][x]
            if c == '.':
                c = ' '
            if c not in ('S', 'E') and (x, y) in nodes:
                c = 'o'
            print(c, end='')
        print()


def solve_part1(grid, is_example):
    start = get_char_pos(grid, 'S')
    end = get_char_pos(grid, 'E')

    pathfind = path(grid, start, end)

    cost = None
    while cost is None:
        pathfind.step()
        cost = pathfind.total_cost

    return cost


def solve_part2(grid, is_example):
    start = get_char_pos(grid, 'S')
    end = get_char_pos(grid, 'E')

    pathfind = path(grid, start, end)

    finished = False
    while not finished:
        finished = pathfind.step()

    num_winning_nodes = pathfind.num_winning_nodes()
    return num_winning_nodes


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
        ('test_input', 1, 7036),
        ('test_input2', 1, 11048),
        ('test_input', 2, 45),
        ('test_input2', 2, 64),
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
    print(f'Solutions found in {took:.3f}s')  # 46657ms  # TODO: still less than a minute!

    # Regression test
    assert part1 == 105508
    assert part2 == 548


if __name__ == '__main__':
    run_examples()
    main()
