class AlmanacRange:
    def __init__(self, dst):
        self.dst = dst
        self.ranges = []

    def add_range(self, range_src, range_dst, range_len):
        self.ranges.append((range(range_src, range_src + range_len), range_dst - range_src))

    def get_destination(self, num):
        for src_range, dst_offset in self.ranges:
            if num in src_range:
                return num + dst_offset, self.dst
        return num, self.dst


def get_range(seeds):
    for i in range(0, len(seeds), 2):
        for seed in range(seeds[i], seeds[i] + seeds[i + 1]):
            yield seed


def solver(input_path, puzzle_type: str):
    assert puzzle_type in ('lowest', 'range')

    seeds = None
    source, destination = None, None
    almanac = {}

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            if line.startswith('seeds'):
                seeds = [int(seed) for seed in line.split()[1:]]
            elif 'map' in line:
                info, _ = line.split()
                source, _, destination = info.split('-')
                almanac[source] = AlmanacRange(destination)
            elif len(line) > 1:
                range_dst, range_src, range_len = line.split()
                range_src, range_dst, range_len = int(range_src), int(range_dst), int(range_len)
                almanac[source].add_range(range_src, range_dst, range_len)

    puzzle_answer = seeds[0]  # fixme
    range_to_use = seeds if puzzle_type == 'lowest' else get_range(seeds)

    for i, seed in enumerate(range_to_use):  # brute force approach, takes ~30mins
        entry = 'seed'
        number = int(seed)
        while entry in almanac:
            number, entry = almanac[entry].get_destination(number)
        puzzle_answer = min(number, puzzle_answer)

    return puzzle_answer


if __name__ == '__main__':
    expected1 = 35
    result1 = solver('test_input', 'lowest')
    assert result1 == expected1, f'Example 1 failed: {result1}'

    expected2 = 46
    result2 = solver('test_input', 'range')
    assert result2 == expected2, f'Example 2 failed: {result2}'

    print("Examples passed")
    print("Puzzle 1 answer:", solver('input', 'lowest'))
    print("Puzzle 2 answer:", solver('input', 'range'))

