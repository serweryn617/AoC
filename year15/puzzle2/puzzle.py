def loader(input_path):
    for line in open(input_path, 'r'):
        width, height, depth = line.strip().split('x')
        yield int(width), int(height), int(depth)


def wrapping_paper_area(width, height, depth):
    faces = width * height, height * depth, width * depth
    area = sum(faces * 2, min(faces))
    return area


def ribbon_length(width, height, depth):
    tie_length = width * height * depth
    
    perimeters = (
        2 * (width + height),
        2 * (height + depth),
        2 * (width + depth),
    )

    return tie_length + min(perimeters)


def solver(input_path, puzzle_type):
    assert puzzle_type in ('part1', 'part2')

    data = loader(input_path)
    
    if puzzle_type == 'part1':
        result = sum(wrapping_paper_area(*present) for present in data)
    else:
        result = sum(ribbon_length(*present) for present in data)

    return result


def run_examples():
    examples = (
        ('test_input', 'part1', 58 + 43),
        ('test_input', 'part2', 34 + 14),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'part1')
    part2 = solver('input', 'part2')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # <1ms

    # Regression test
    assert part1 == 1588178
    assert part2 == 3783758


if __name__ == '__main__':
    run_examples()
    main()

