from math import prod


class FlipFlop:
    def __init__(self, targets):
        self.state = 0
        self.targets = targets

    def get_output(self, pulse, source):
        if pulse == 1:
            return

        self.state ^= 1
        return self.targets, self.state

class Conjunction:
    def __init__(self, targets):
        self.targets = targets
        self.inputs = {}

    def add_input(self, source):
        self.inputs[source] = 0

    def get_output(self, pulse, source):
        self.inputs[source] = pulse

        send = not all(self.inputs.values())
        return self.targets, send

class TestModule:
    def __init__(self):
        self.targets = []

    def get_output(self, pulse, source):
        return None


def get_conjunction_inputs(modules):
    for name, module in modules.items():
        if isinstance(module, Conjunction):
            inputs = list(filter(lambda x: name in x[1].targets, modules.items()))
            for i in inputs:
                module.add_input(i[0])


def get_conjunctor_name(search, modules):
    for name, module in modules.items():
        if search in module.targets:
            assert isinstance(module, Conjunction), f'Module outputting to {search} is not a Conjunctor!'
            return name


def loader(input_path):
    modules = {}

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            config, _, *targets = line.replace(',', '').split()
            
            if config == 'broadcaster':
                initial = [('broadcaster', t, 0) for t in targets]
                continue

            mod_type = config[0]
            mod_name = config[1:]

            if mod_type == '%':
                modules[mod_name] = FlipFlop(targets)
            elif mod_type == '&':
                modules[mod_name] = Conjunction(targets)

    return modules, initial


def solver(input_path, puzzle_type):
    assert puzzle_type in ('pulses', 'rx')

    button_presses = 1000

    modules, initial = loader(input_path)
    get_conjunction_inputs(modules)

    modules['output'] = TestModule()
    modules['rx'] = TestModule()

    num_low = 0
    num_high = 0

    # for part 2 assume that rx is driven by 1 and only 1 conjuntor
    # whose inputs state cycles periodically from the beginning
    # and are set to high only once per period in the last cycle
    if puzzle_type == 'rx':
        button_presses = 10000  # must be greater than each input cycle
        rx_conjunctor = get_conjunctor_name('rx', modules)
        cycles = {k: {'presses': 0, 'delta': 0} for k in modules[rx_conjunctor].inputs}

    for num_presses in range(1, button_presses + 1):
        inputs = initial.copy()
        num_low += len(initial) + 1

        while inputs:
            source, name, pulse = inputs.pop(0)

            if puzzle_type == 'rx' and name == rx_conjunctor and pulse == True:
                cycles[source]['delta'] = num_presses - cycles[source]['presses']
                cycles[source]['presses'] = num_presses
                deltas = [i['delta'] for i in cycles.values()]
                if all(deltas):
                    return prod(deltas)

            result = modules[name].get_output(pulse, source)

            if result is None:
                continue

            targets, pulse = result
            inputs += [(name, t, pulse) for t in targets]

            if pulse:
                num_high += len(targets)
            else:
                num_low += len(targets)

    return num_high * num_low


def run_examples():
    examples = (
        ('test_input1', 'pulses', 32000000),
        ('test_input2', 'pulses', 11687500),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'pulses')
    part2 = solver('input', 'rx')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 65ms

    # Regression test
    assert part1 == 836127690
    assert part2 == 240914003753369


if __name__ == '__main__':
    run_examples()
    main()
