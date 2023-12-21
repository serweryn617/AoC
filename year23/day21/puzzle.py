class FillPaths:
    DIRECTIONS = (
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
    )
    TRAVERSIBLE = '.'

    def __init__(self, grid, start):
        self.grid = grid
        self.edge_tiles = [start]
        self.visited_tiles = {start: 0}
        self.distance = 0

    def _is_traversible(self, tile):
        y, x = tile
        y %= len(self.grid)
        x %= len(self.grid[0])
        tile_type = self.grid[y][x]
        return tile_type == self.TRAVERSIBLE

    def _step(self):
        new_edge_tiles = []
        self.distance += 1

        for y, x in self.edge_tiles:
            for dy, dx in self.DIRECTIONS:
                tile = y + dy, x + dx

                if self._is_traversible(tile) and tile not in self.visited_tiles:
                    new_edge_tiles.append(tile)
                    self.visited_tiles[tile] = self.distance

        self.edge_tiles = new_edge_tiles

    def take_steps(self, num_steps):
        for _ in range(num_steps):
            self._step()

    def even_tiles(self):
        return [key for key, val in self.visited_tiles.items() if val % 2 == 0]

    def odd_tiles(self):
        return [key for key, val in self.visited_tiles.items() if val % 2 == 1]


def get_starting_pos(grid):
    for y, row in enumerate(grid):
        x = row.find('S')
        if x >= 0:
            grid[y] = row[:x] + '.' + row[x + 1:]
            return y, x


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        grid = [line.strip() for line in puzzle.readlines()]

    return grid


def solver(input_path, num_steps):
    grid = loader(input_path)
    
    start = get_starting_pos(grid)

    a = FillPaths(grid, start)
    a.take_steps(num_steps)

    # for y, row in enumerate(grid):
    #     for x, c in enumerate(row):
    #         if (y, x) in a.even_tiles():
    #             print('O', end='')
    #         else:
    #             print(c, end='')
    #     print()

    if num_steps % 2:
        puzzle_answer = len(a.odd_tiles())
    else:
        puzzle_answer = len(a.even_tiles())

    return puzzle_answer


def run_examples():
    examples = (
        # ('test_input', 6, 16),
        # ('test_input', 10, 50),
        # ('test_input', 50, 1594),
        # ('test_input', 100, 6536),
        # ('test_input', 500, 167004),
        # ('test_input', 1000, 668697),
        ('test_input', 5000, 16733044),
    )

    for path, num_steps, expected in examples:
        result = solver(path, num_steps)
        assert result == expected, f'Example {path} {num_steps} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 64)
    part2 = solver('input', 26501365)

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Solution found in {took:.3f}s')  # 5ms

    # Regression test
    assert part1 == 3731
    # assert part2 == 


if __name__ == '__main__':
    run_examples()
    main()
