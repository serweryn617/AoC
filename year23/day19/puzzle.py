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
            self.value = int(expression[2:])
            self.output = output
            self.default = None

    def check(self, data):
        if self.default is not None:
            return self.default
        else:
            result = self.comparator(data[self.key], self.value)
            return self.output if result else None


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


def run_examples():
    examples = (
        ('test_input', 'list', 19114),
        # ('test_input', 'combinations', 167409079868000),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'list')
    # part2 = solver('input', 'combinations')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    # print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 2ms

    # Regression test
    assert part1 == 19114
    # assert part2 == 


if __name__ == '__main__':
    run_examples()
    main()
