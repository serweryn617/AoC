from dataclasses import dataclass


def is_file(n):
    return n % 2 == 0


def file_id(n):
    return n // 2


def gen_start(data):
    for sp in range(len(data)):
        start = int(data[sp])

        for _ in range(start):
            yield sp, is_file(sp), file_id(sp)

        sp += 1


def gen_end(data):
    for ep in range(len(data) - 1, 0, -1):
        end = int(data[ep])

        if is_file(ep):
            for _ in range(end):
                yield ep, file_id(ep)

        ep -= 1


def gen_blocks(data):
    current_end_gen = gen_end(data)
    ep = len(data) - 1

    for sp, s_file, s_id in gen_start(data):
        if s_file:
            yield s_id

            if ep <= sp:
                return
        else:
            ep, e_id = next(current_end_gen)

            if ep <= sp:
                return

            yield e_id


def solve_part1(parsed_input):
    total = 0

    for p, val in enumerate(gen_blocks(parsed_input)):
        total += p * val

    return total


@dataclass
class Block:
    file: bool
    size: int
    id_: int
    skip: int = False


def parsed_blocks(data):
    blocks = []

    for idx in range(len(data)):
        size = int(data[idx])
        blocks.append(Block(is_file(idx), size, file_id(idx)))

    return blocks


def first_fit_idx(data, size):
    for i in range(len(data)):
        block = data[i]
        if not block.file and block.size >= size:
            return i


def last_file_idx(data):
    for i in reversed(range(len(data))):
        block = data[i]
        if block.file and not block.skip:
            return i


def print_blocks(blocks):
    for b in blocks:
        for _ in range(b.size):
            if b.file:
                print(b.id_, end='')
            else:
                print('.', end='')
    print()


def solve_part2(parsed_input):
    blocks = parsed_blocks(parsed_input)

    while True:
        file_idx = last_file_idx(blocks)
        if file_idx is None:
            break

        file = blocks[file_idx]
        file.skip = True
        free_idx = first_fit_idx(blocks, file.size)

        if free_idx is not None and free_idx < file_idx:
            fit = blocks[free_idx]
            file = blocks[file_idx]
            new_file = Block(file.file, file.size, file.id_)

            fit.size -= file.size
            file.file = False

            blocks.insert(free_idx, new_file)

    total = 0
    idx = 0
    for b in blocks:
        for _ in range(b.size):
            if b.file:
                total += b.id_ * idx
            idx += 1

    return total


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        puzzle_input = puzzle.readline().strip()

    return puzzle_input


def solver(input_path, part):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input)
    else:
        result = solve_part2(parsed_input)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 1928),
        ('test_input', 2, 2858),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    sp_time = time.time()

    part1 = solver('input', 1)
    part2 = solver('input', 2)

    took = time.time() - sp_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Solutions found in {took:.3f}s')  # 7118ms  TODO: better method?

    # Regression test
    assert part1 == 6519155389266
    assert part2 == 6547228115826


if __name__ == '__main__':
    run_examples()
    main()
