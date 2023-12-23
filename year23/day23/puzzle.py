PASSIBLE = '.'
SLOPES = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}


class Trail:
    def __init__(self, start):
        self.start = start[:2]
        self.start_dir = None
        self.end = None

        if len(start) == 4:
            self.start_dir = start[2:]

        self.length = 0
        self.longest_path = -1
        self.reached_end = False

        self.next_starts = []
        self.next_trails = []
        self.prev_trails = []

    def sort_key(self):
        return self.longest_path, self.length

    def link_trail(self, trail):
        self.next_trails.append(trail)

    def get_trail_length(self, grid):
        pos = self.start
        visited = [pos]

        if self.start_dir is None:
            tile = grid[pos[0]][pos[1]]
            if tile in SLOPES:
                dy, dx = SLOPES[tile]
                pos = pos[0] + dy, pos[1] + dx
                visited.append(pos)
        else:
            dy, dx = self.start_dir
            pos = pos[0] + dy, pos[1] + dx
            visited.append(pos)

        while not self.reached_end:
            for dy, dx in SLOPES.values():
                new_pos = pos[0] + dy, pos[1] + dx

                if new_pos[0] >= len(grid):
                    self.reached_end = True
                    break

                tile = grid[new_pos[0]][new_pos[1]]
                if tile == PASSIBLE and new_pos not in visited:
                    pos = new_pos
                    visited.append(pos)
                    break
            else:
                break

        self.length = len(visited)
        self.end = pos

    def find_next_starts(self, grid, directed=True):
        next_start_dir = None

        for key, (dy, dx) in SLOPES.items():
            new_pos = self.end[0] + dy, self.end[1] + dx

            if new_pos[0] >= len(grid):
                continue

            tile = grid[new_pos[0]][new_pos[1]]
            if directed and tile == key:
                next_start_dir = dy, dx
                self.next_starts.append(new_pos)
            elif not directed and tile in SLOPES:
                next_start_dir = dy, dx
                self.next_starts.append(new_pos + next_start_dir)

        if len(self.next_starts) == 1:
            dy, dx = next_start_dir
            self.length += 1
            self.end = self.end[0] + dy, self.end[1] + dx
            self.next_starts[0] = self.end[0] + dy, self.end[1] + dx


def find_longest_path(start, trails):
    # Modified Djikstra's Algorithm

    trails[start].longest_path = 0
    not_visited = list(trails.values())
    not_visited.sort(key=Trail.sort_key, reverse=True)

    while not_visited:
        trail = not_visited[0]
        length = trail.longest_path + trail.length

        for next_trail in trail.next_trails:
            if length > next_trail.longest_path:
                next_trail.longest_path = length

                # Assume there is no loops
                if next_trail not in not_visited:
                    not_visited.append(next_trail)

        not_visited.pop(0)
        not_visited.sort(key=Trail.sort_key, reverse=True)


def init_trails(start, grid, trails, directed):
    enterances = [start]

    while enterances:
        pos = enterances[0]

        if pos not in trails:
            nt = Trail(pos)
            trails[pos[:2]] = nt

            nt.get_trail_length(grid)
            nt.find_next_starts(grid, directed)
            enterances += nt.next_starts

            if nt.reached_end:
                end_trail = nt

        enterances.pop(0)

    return end_trail


def link_trails(trails):
    for trail in trails.values():
        for start in trail.next_starts:
            trail.link_trail(trails[start[:2]])


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        grid = puzzle.readlines()

    return grid


def solver(input_path, puzzle_type):
    assert puzzle_type in ('slopes', 'longest')

    grid = loader(input_path)
    start = 0, grid[0].find(PASSIBLE)
    assert start[1] >= 0, 'Starting position not found'

    trails = {}
    directed = puzzle_type == 'slopes'
    end_trail = init_trails(start, grid, trails, directed)
    link_trails(trails)
    find_longest_path(start, trails)

    longest_path = end_trail.longest_path + end_trail.length - 1
    return longest_path


def run_examples():
    examples = (
        ('test_input', 'slopes', 94),
        # ('test_input', 'longest', 154),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'slopes')
    # part2 = solver('input', 'longest')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    # print('Puzzle 2 answer:', part2)
    print(f'Solution found in {took:.3f}s')  # 14ms

    # Regression test
    assert part1 == 2042
    # assert part2 == 


if __name__ == '__main__':
    run_examples()
    main()
