class bfs_pathfind:
    def __init__(self, map_, start, end):
        self.map = map_
        self.max = len(self.map[0]) - 1, len(self.map) - 1

        self.heads = [start]
        self.end = end
        self.visited = [start]

        self.steps = 0

    def get_valid_steps(self, pos):
        x, y = pos
        max_x, max_y = self.max
        max_height = self.map[y][x] + 1

        next_steps = []
        if x > 0 and self.map[y][x-1] <= max_height and (x-1, y) not in self.visited:
            next_steps.append((x-1, y))
        if x < max_x and self.map[y][x+1] <= max_height and (x+1, y) not in self.visited:
            next_steps.append((x+1, y))
        if y > 0 and self.map[y-1][x] <= max_height and (x, y-1) not in self.visited:
            next_steps.append((x, y-1))
        if y < max_y and self.map[y+1][x] <= max_height and (x, y+1) not in self.visited:
            next_steps.append((x, y+1))

        return next_steps

    def step(self):
        next_heads = []
        for head in self.heads:
            next_steps = self.get_valid_steps(head)
            self.visited.extend(next_steps)
            next_heads.extend(next_steps)

        self.heads = next_heads
        self.steps += 1

    def reached_end(self):
        return self.end in self.visited

    def reached_height(self, height):
        heights = [self.map[y][x] for x, y in self.visited]
        return height in heights


def parse(data):
    map_ = []
    for y, line in enumerate(data):
        row = []
        for x, c in enumerate(line.strip()):
            if c == 'S':
                start = x, y
                height = 0
            elif c == 'E':
                end = x, y
                height = ord('z') - ord('a')
            else:
                height = ord(c) - ord('a')
            row.append(height)
        map_.append(row)
    return map_, start, end


def reverse_height(map_):
    new_map = []
    for line in map_:
        row = [ord('z') - h for h in line]
        new_map.append(row)
    return new_map


def solver(input_path, part):
    with open(input_path, 'r') as puzzle:
        puzzle_input = puzzle.readlines()

    map_, start, end = parse(puzzle_input)

    if part == 1:
        condition = lambda x: not x.reached_end()
    else:
        map_ = reverse_height(map_)
        start, end = end, start
        condition = lambda x: not x.reached_height(ord('z'))

    pathfinder = bfs_pathfind(map_, start, end)

    while condition(pathfinder):
        pathfinder.step()

    return pathfinder.steps


if __name__ == '__main__':
    expected1 = 31
    result1 = solver('test_input', 1)
    assert result1 == expected1, f'Example 1 failed: {result1}'

    expected2 = 29
    result2 = solver('test_input', 2)
    assert result2 == expected2, f'Example 2 failed: {result2}'

    print("Examples passed")
    print("Puzzle 1 answer:", solver('input', 1))
    print("Puzzle 2 answer:", solver('input', 2))
