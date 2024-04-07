WORD_MASK = 0xffff


class Gate:
    def __init__(self, output, inputs):
        self.output = output
        self.input = {i: None if isinstance(i, str) else i for i in inputs}

    def get_input_names(self):
        return self.input.keys()

    def activate_input(self, input_name, value):
        assert input_name in self.input
        self.input[input_name] = value

    def get_output(self):
        values = self.input.values()
        none_values = [v is None for v in values]

        if any(none_values):
            return None, None

        value = self._gate_func(list(values)) & WORD_MASK
        return self.output, value


class Not(Gate):
    def _gate_func(self, values):
        assert len(values) == 1
        return values[0] ^ WORD_MASK


class And(Gate):
    def _gate_func(self, values):
        assert len(values) == 2
        return values[0] & values[1]


class Or(Gate):
    def _gate_func(self, values):
        assert len(values) == 2
        return values[0] | values[1]


class LShift(Gate):
    def _gate_func(self, values):
        assert len(values) == 2
        return values[0] << values[1]


class RShift(Gate):
    def _gate_func(self, values):
        assert len(values) == 2
        return values[0] >> values[1]


class Wire(Gate):
    def _gate_func(self, values):
        assert len(values) == 1
        return values[0]


def loader(input_path):
    for line in open(input_path, 'r'):
        *source, _, output = line.split()
        
        for i in range(len(source)):
            try:
                source[i] = int(source[i])
            except ValueError:
                pass
        
        yield source, output


def solver(input_path, puzzle_type):
    assert puzzle_type in ('part1', 'part2')

    data = loader(input_path)

    gates = []
    signals = {}

    for source, output in data:
        if len(source) == 1 and isinstance(source[0], int):
            signals[output] = source[0]
        elif 'NOT' in source:
            inputs = (source[1],)
            gates.append(Not(output, inputs))
        elif 'AND' in source:
            inputs = source[0], source[2]
            gates.append(And(output, inputs))
        elif 'OR' in source:
            inputs = source[0], source[2]
            gates.append(Or(output, inputs))
        elif 'LSHIFT' in source:
            inputs = source[0], source[2]
            gates.append(LShift(output, inputs))
        elif 'RSHIFT' in source:
            inputs = source[0], source[2]
            gates.append(RShift(output, inputs))
        else:  # wire
            inputs = (source[0],)
            gates.append(Wire(output, inputs))

    while 'a' not in signals:
        to_pop = []

        for idx in range(len(gates)):
            gate = gates[idx]
            inputs = gate.get_input_names()
            for i in inputs:
                if i in signals:
                    gate.activate_input(i, signals[i])

            output, value = gate.get_output()
            if value is not None:
                signals[output] = value
                to_pop.append(idx)
        
        for idx in reversed(to_pop):
            gates.pop(idx)

    return signals['a']

    # if puzzle_type == 'part1':
        # for i in data:
        #     print(i)
    # else:
        


def run_examples():
    examples = (
        ('test_input', 'part1', 72),
        # ('test_input', 'part2', 1000*1000*1 + 1000*2 - 4),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'part1')
    # part2 = solver('input', 'part2')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    # print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 8ms

    # Regression test
    assert part1 == 956
    # assert part2 == 14110788


if __name__ == '__main__':
    run_examples()
    main()
