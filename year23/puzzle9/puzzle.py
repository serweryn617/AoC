from math import comb


def pascals_triangle(n):
    return [comb(n, i) for i in range(n + 1)]


def oasis_coeff(n, direction = 'forward'):
    coeff = pascals_triangle(n)

    for i in range(0, len(coeff), 2):
        coeff[i] *= -1

    if direction == 'forward':
        # last coefficient has to be -1
        coeff.reverse()
        return coeff[:-1]  # skip last one
    elif direction == 'backward':
        # first coefficient has to be -1
        return coeff[1:]  # skip first one


def sumprod(a, b):
    prod = [a[i] * b[i] for i in range(len(a))]
    return sum(prod)


def get_next_number(seq):
    seq_len = len(seq)
    coeff = oasis_coeff(seq_len)
    return sumprod(seq, coeff)


def get_prev_number(seq):
    seq_len = len(seq)
    coeff = oasis_coeff(seq_len, 'backward')
    return sumprod(seq, coeff)


def solver(input_path, puzzle_type: str):
    assert puzzle_type in ('history', 'backward')

    puzzle_answer = 0

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            sequence = [int(s) for s in line.split()]

            if puzzle_type == 'history':
                puzzle_answer += get_next_number(sequence)
            elif puzzle_type == 'backward':
                puzzle_answer += get_prev_number(sequence)

    return puzzle_answer


def run_examples():
    examples = (
        ('test_input', 'history', 114),
        ('test_input', 'backward', 2),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} failed: {result}'

    print('Examples passed')


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'history')
    part2 = solver('input', 'backward')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 1ms

    # Regression test
    assert part1 == 2008960228
    assert part2 == 1097


if __name__ == '__main__':
    run_examples()
    main()