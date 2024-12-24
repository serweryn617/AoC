OPS = {
    'OR': lambda x, y: x or y,
    'AND': lambda x, y: x and y,
    'XOR': lambda x, y: x ^ y,
}


def get_all_outputs(operations):
    outputs = []

    for operation in operations:
        s1, s2, _, out = operation
        for signal in (s1, s2, out):
            if signal.startswith('z'):
                outputs.append(signal)

    return set(outputs)


def simulate(signals, operations):
    for i in range(len(operations)):
        s1, s2, op, out = operations[i]

        if not set((s1, s2)).issubset(signals):
            continue

        operations.pop(i)

        s1 = signals[s1]
        s2 = signals[s2]

        signals[out] = OPS[op](s1, s2)
        break


def combine_binary(outputs, signals):
    result = 0

    for out in outputs:
        offset = int(out[1:])
        value = signals[out]

        result |= value << offset

    return result


def solve_part1(parsed_input, is_example):
    signals, operations = parsed_input

    outputs = get_all_outputs(operations)

    while not outputs.issubset(signals):
        simulate(signals, operations)

    result = combine_binary(outputs, signals)
    return result


class FullAdder:
    def __init__(self, i1, i2, out, and_gates, or_gates, xor_gates):
        self.a = min(i1, i2)
        self.b = max(i1, i2)
        self.out = out

        self.and_gates = and_gates
        self.or_gates = or_gates
        self.xor_gates = xor_gates

        self.carry_in = None
        self.carry_out = None

    def intermediate(self, swapped):  # TODO: there's many assumptions and it's too complex
        carry1 = self.and_gates[(self.a, self.b)]
        output1 = self.xor_gates[(self.a, self.b)]

        out_xor_in = [k for k, v in self.xor_gates.items() if v == self.out]
        if not out_xor_in:
            # approx carry in
            out_xor_gate = [(k, v) for k, v in self.xor_gates.items() if output1 in k]
            out_xor_in, val = out_xor_gate[0]
            out_xor_in = [out_xor_in]

            print(self.out, '-- swapped --', val)
            swapped.append(self.out)
            swapped.append(val)
        out_xor_in = list(out_xor_in[0])

        if output1 not in out_xor_in:
            # output1 or self.out, in my case it's output1

            # approx output1
            a, b = out_xor_in
            if a in self.or_gates.values():
                print(output1, '-- swapped --', b)
                swapped.append(output1)
                swapped.append(b)
                output1 = b
            else:
                print(output1, '-- swapped --', a)
                swapped.append(output1)
                swapped.append(a)
                output1 = a

        out_xor_in.remove(output1)
        self.carry_in = out_xor_in[0]

        carry_key = tuple(sorted([self.carry_in, output1]))
        carry2 = self.and_gates[carry_key]

        carry_key = tuple(sorted([carry1, carry2]))
        if carry_key not in self.or_gates:

            # approx carry out
            a = [v for k, v in self.or_gates.items() if carry1 in k]
            if a:
                self.carry_out = a[0]
                return

            b = [v for k, v in self.or_gates.items() if carry2 in k]
            if b:
                self.carry_out = b[0]
                return

        self.carry_out = self.or_gates[carry_key]


def solve_part2(parsed_input, is_example):
    # NOTE: Assume the circuit is just standard half/full adder chain
    signals, gates = parsed_input

    and_gates = {tuple(sorted((s1, s2))): out for s1, s2, op, out in gates if op == 'AND'}
    or_gates = {tuple(sorted((s1, s2))): out for s1, s2, op, out in gates if op == 'OR'}
    xor_gates = {tuple(sorted((s1, s2))): out for s1, s2, op, out in gates if op == 'XOR'}

    x_bits = [s for s in signals if s.startswith('x')]
    y_bits = [s for s in signals if s.startswith('y')]
    z_bits = list(get_all_outputs(gates))

    assert len(x_bits) == len(y_bits) == len(z_bits) - 1

    x_bits.sort()
    y_bits.sort()
    z_bits.sort()

    carry_in = and_gates[(x_bits[0], y_bits[0])]
    assert z_bits[0] == xor_gates[(x_bits[0], y_bits[0])]

    swapped = []

    for i in range(1, len(x_bits)):
        x = x_bits[i]
        y = y_bits[i]
        z = z_bits[i]

        adder = FullAdder(x, y, z, and_gates, or_gates, xor_gates)
        adder.intermediate(swapped)

        if adder.carry_in != carry_in:
            print('Carry mismatch', adder.carry_in, carry_in)

        carry_in = adder.carry_out

    return ','.join(sorted(swapped))


def loader(input_path):
    signals = {}
    operations = []

    with open(input_path, 'r') as puzzle:
        line = puzzle.readline().strip()
        while line:
            wire, value = line.split(': ')
            value = bool(int(value))
            signals[wire] = value
            line = puzzle.readline().strip()

        for line in puzzle.readlines():
            s1, op, s2, _, out = line.split()
            operations.append((s1, s2, op, out))

    return signals, operations


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, 2024),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type, is_example=True)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 1)
    part2 = solver('input', 2)

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Solutions found in {took:.3f}s')  # 0ms

    # Regression test
    assert part1 == 49574189473968
    assert part2 == 'ckb,kbs,ksv,nbd,tqq,z06,z20,z39'


if __name__ == '__main__':
    run_examples()
    main()
