from math import lcm


def parse(data, divide):
    monkeys = {}
    monkey_desc_len = 5
    for n, line in enumerate(data):
        if line.startswith("Monkey"):
            num = int(line.strip()[:-1].split()[-1])
            next_line_num = n+1
            m = make_monkey(data[next_line_num:next_line_num+monkey_desc_len], divide)
            monkeys[num] = m
    return monkeys


def make_monkey(desc, divide):
    items = desc[0]
    assert "Starting items:" in items
    items = items.replace(',', '').split()[2:]
    items = [int(i) for i in items]

    operation_desc = desc[1]
    assert "Operation: new = old" in operation_desc
    operation_desc = operation_desc.split()[-2:]

    if operation_desc[1] == "old":
        old_ops = {
            '+': lambda x: x + x,
            '*': lambda x: x * x,
        }
        operation = old_ops[operation_desc[0]]
    else:
        n = int(operation_desc[1])
        abs_ops = {
            '+': lambda x: x + n,
            '*': lambda x: x * n,
        }
        operation = abs_ops[operation_desc[0]]

    test_desc = desc[2]
    assert "Test: divisible by" in test_desc
    test = int(test_desc.split()[-1])

    on_true = desc[3]
    assert "If true: throw to monkey" in on_true
    on_true = int(on_true.split()[-1])

    on_false = desc[4]
    assert "If false: throw to monkey" in on_false
    on_false = int(on_false.split()[-1])

    return monkey(items, operation, test, on_true, on_false, divide=divide)


class monkey:
    def __init__(self, items, operation, test, on_true, on_false, *, divide=True):
        self.items = items
        self.operation = operation
        self.test = test
        self.on_true = on_true
        self.on_false = on_false
        self.divide = divide

        self.inspections = 0
        self.limit = None

    def throw_item(self):
        self.inspections += 1

        item = self.items.pop(0)
        item = self.operation(item)

        item = item % self.limit

        if self.divide:
            item = item // 3

        res = item % self.test == 0
        throw_to = self.on_true if res else self.on_false
        return throw_to, item

    def catch_item(self, item):
        self.items.append(item)


def round(monkeys):
    for m in monkeys.values():
        while m.items:
            throw_to, item = m.throw_item()
            monkeys[throw_to].catch_item(item)


def solver(input_path, part):
    if part == 0:
        rounds = 20
        divide = True
    else:
        rounds = 10000
        divide = False

    with open(input_path, 'r') as puzzle:
        puzzle_input = puzzle.readlines()

    monkeys = parse(puzzle_input, divide)
    limit = lcm(*(m.test for m in monkeys.values()))
    for m in monkeys.values():
        m.limit = limit

    for _ in range(rounds):
        round(monkeys)

    inspections = [m.inspections for m in monkeys.values()]
    inspections.sort(reverse=True)
    total = inspections[0] * inspections[1]

    return total


if __name__ == '__main__':
    expected1 = 10605
    result1 = solver('test_input', 0)
    assert result1 == expected1, f'Example 1 failed: {result1}'

    expected2 = 2713310158
    result2 = solver('test_input', 1)
    assert result2 == expected2, f'Example 2 failed: {result2}'

    print("Examples passed")
    print("Puzzle 1 answer:", solver('input', 0))
    print("Puzzle 2 answer:", solver('input', 1))
