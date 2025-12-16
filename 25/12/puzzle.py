def is_impossible(size, num_shapes, shape_areas):
    min_area = sum((a * n for a, n in zip(shape_areas, num_shapes)))
    x, y = size
    return min_area > (x * y)


def num_maybe_possible(areas_spec, shape_areas):
    num = len(areas_spec)
    for size, num_shapes in areas_spec:
        if is_impossible(size, num_shapes, shape_areas):
            num -= 1
    return num


def solve(parsed_input):
    shapes, areas_spec = parsed_input
    shape_areas = []
    for v in shapes:
        shape_area = sum((s.count("#") for s in v))
        shape_areas.append(shape_area)

    n = num_maybe_possible(areas_spec, shape_areas)
    return n


def parser(data):
    shapes = {}
    areas = []
    shape_num = None

    for line in data:
        if "x" in line:
            size, *nums = line.split()
            x, y = size.strip(":").split("x")
            area = ((int(x), int(y)), tuple(map(int, nums)))
            areas.append(area)
        elif ":" in line:
            shape_num = int(line.strip(":"))
        elif line:
            if shape_num not in shapes:
                shapes[shape_num] = [line]
            else:
                shapes[shape_num].append(line)

    shapes_list = [s for _, s in sorted(shapes.items(), key=lambda i: i[0])]
    return shapes_list, areas


def loader(input_path):
    data = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle:
            data.append(line.strip())

    return parser(data)


def solver(input_path):
    parsed_input = loader(input_path)
    return solve(parsed_input)


def main():
    import time
    start_time = time.time()

    part1 = solver('input')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print(f'Solutions found in {took:.3f}s')  # 2ms

    # Regression test
    assert part1 == 510


if __name__ == '__main__':
    # NOTE: solution cheesed; examples don't work :)
    main()
