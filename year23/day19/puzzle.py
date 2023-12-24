class Rule:
    COMPARATORS = {
        '<': lambda a, b: a < b,
        '>': lambda a, b: a > b,
    }

    def __init__(self, descriptor):
        if ':' not in descriptor:
            self.default = descriptor
        else:
            expression, output = descriptor.split(':')

            self.key = expression[0]
            self.comparator = self.COMPARATORS[expression[1]]
            self.comparator_raw = expression[1]
            self.value = int(expression[2:])
            self.output = output
            self.default = None

    def check(self, data):
        if self.default is not None:
            return self.default
        else:
            result = self.comparator(data[self.key], self.value)
            return self.output if result else None


def num_combinations(xmas):
    x, m, a, s = xmas
    # ranges are inclusive: (1:4000) yields 4000 combinations
    x = x[1] - x[0] + 1
    m = m[1] - m[0] + 1
    a = a[1] - a[0] + 1
    s = s[1] - s[0] + 1
    return x * m * a * s


def new_range(original, min_value=None, max_value=None):
    lower, upper, = original

    if min_value is not None:
        lower = max(lower, min_value)
    if max_value is not None:
        upper = min(upper, max_value)

    return lower, upper


def traverse(node, workflows, combinations, xmas):
    keys = {'x': 0, 'm': 1, 'a': 2, 's': 3}

    for rn, rule in enumerate(workflows[node]):
        if rule.default == 'A':
            combinations.append(num_combinations(xmas))
            return
        elif rule.default == 'R':
            return
        elif rule.default is not None:
            traverse(rule.default, workflows, combinations, xmas)
            return

        idx = keys[rule.key]

        if rule.comparator_raw == '<':
            new = new_range(xmas[idx], max_value = rule.value - 1)
            old = new_range(xmas[idx], min_value = rule.value)
        else:
            new = new_range(xmas[idx], min_value = rule.value + 1)
            old = new_range(xmas[idx], max_value = rule.value)

        new_xmas = xmas[:idx] + (new,) + xmas[idx + 1:]
        xmas = xmas[:idx] + (old,) + xmas[idx + 1:]

        traverse(rule.output, workflows, combinations, new_xmas)


def process_list(workflows, ratings):
    total = 0

    for r in ratings:
        result = 'in'
        while result not in ('A', 'R'):

            for rule in workflows[result]:
                out = rule.check(r)
                if out is not None:
                    break

            result = out
        if result == 'A':
            total += sum(r.values())

    return total


def loader(input_path):
    workflows = {}
    ratings = []

    with open(input_path, 'r') as puzzle:
        line = puzzle.readline().strip()
        while line:
            name, rules = line.split('{')
            rules = rules[:-1].split(',')
            workflows[name] = [Rule(desc) for desc in rules]
            line = puzzle.readline().strip()

        line = puzzle.readline().strip()
        while line:
            line = line[1:-1].split(',')
            categories = dict([(desc[0], int(desc[2:])) for desc in line])
            ratings.append(categories)
            line = puzzle.readline().strip()

    return workflows, ratings


def solver(input_path, puzzle_type):
    assert puzzle_type in ('list', 'combinations')

    workflows, ratings = loader(input_path)

    if puzzle_type == 'list':
        total = process_list(workflows, ratings)
    else:
        workflows['A'] = [Rule('A')]
        workflows['R'] = [Rule('R')]
        combinations = []

        traverse('in', workflows, combinations, ((1, 4000), (1, 4000), (1, 4000), (1, 4000)))
        total = sum(combinations)

    return total


def run_examples():
    examples = (
        ('test_input', 'list', 19114),
        ('test_input', 'combinations', 167409079868000),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'list')
    part2 = solver('input', 'combinations')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 3ms

    # Regression test
    assert part1 == 418498
    assert part2 == 123331556462603


if __name__ == '__main__':
    run_examples()
    main()
