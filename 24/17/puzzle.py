class ternary_cpu:
    def __init__(self, a, b, c):
        self.init_a = a
        self.init_b = b
        self.init_c = c

        self.opcodes = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

        self.reset()

    def reset(self):
        self.a = self.init_a
        self.b = self.init_b
        self.c = self.init_c

        self.pc = 0
        self.output = []
        self.halted = False

    def load(self, prog):
        self.prog = prog

    def step(self):
        if self.pc + 1 >= len(self.prog) or self.halted:
            self.halted = True
            return

        ins = self.prog[self.pc]
        op = self.prog[self.pc + 1]
        self.pc += 2

        func = self.opcodes[ins]
        func(op)

    def combo(self, op):
        if op <= 3:
            return op
        if op == 4:
            return self.a
        if op == 5:
            return self.b
        if op == 6:
            return self.c
        raise ValueError

    def adv(self, op):
        exp = self.combo(op)
        self.a = self.a >> exp

    def bxl(self, op):
        self.b = self.b ^ op

    def bst(self, op):
        val = self.combo(op)
        self.b = val % 8

    def jnz(self, op):
        if self.a:
            self.pc = op

    def bxc(self, op):
        self.b = self.b ^ self.c

    def out(self, op):
        val = self.combo(op)
        self.output.append(val % 8)

    def bdv(self, op):
        exp = self.combo(op)
        self.b = self.a >> exp

    def cdv(self, op):
        exp = self.combo(op)
        self.c = self.a >> exp


def solve_part1(parsed_input, is_example):
    reg_a, reg_b, reg_c, prog = parsed_input
    cpu = ternary_cpu(reg_a, reg_b, reg_c)
    cpu.load(prog)

    while not cpu.halted:
        cpu.step()

    out = cpu.output
    return ','.join(map(str, out))


def check_c_valid(a, c):
    offset = (a & 0b111) ^ 0b1

    a_bits = make_bit_dict(a, 3)
    c_bits = make_bit_dict(c, 3, offset)

    bits = combine_bit_dicts(a_bits, c_bits)
    return bits


def make_bit_dict(x, length, base=0):
    bit_dict = {}
    for n in range(length):
        bit = (x >> n) & 0b1
        bit_dict[n + base] = bit
    return bit_dict


def combine_bit_dicts(a, b):
    d = a.copy()
    for k, v in a.items():
        if k in b and b[k] != v:
            return
    d.update(b)
    return d


def value_from_bit_dict(d):
    val = 0
    for k, v in d.items():
        val |= v << k
    return val


def get_loop_value(a):
    b = (a & 0b111) ^ 0b1
    c = a >> b
    b = b ^ c
    b = b ^ 6
    return b & 0b111


def offset_bit_dict(d, offset):
    new_dict = {}
    for k, v in d.items():
        new_dict[k + offset] = v
    return new_dict


def combine(current, possible_values, program, results):
    current = current or {}

    if not program:
        results.append(current)
        return

    current = offset_bit_dict(current, 3)
    key = program[0]
    for val in possible_values[key]:
        bit_dict = combine_bit_dicts(current, val)
        if bit_dict:
            combine(bit_dict, possible_values, program[1:], results)


def run(a, prog):
    cpu = ternary_cpu(a, 0, 0)
    cpu.load(prog)

    while not cpu.halted:
        cpu.step()

    return cpu.output


def solve_part2(parsed_input, is_example):
    # NOTE: I solved this on paper, below is just some helper math

    _, _, _, prog = parsed_input

    assert prog[-4] == 5, 'Previous to last instruction needs to be out!'
    assert prog[-2] == 3, 'Last instruction needs to be jnz!'
    assert prog[-1] == 0, 'Last jnz operand must be 0'

    instr = prog[:-4:2]
    assert 3 not in instr, 'Additional jnz not supported!'
    assert 5 not in instr, 'Additional out not supported!'

    # Other assumptions:
    # B and C starting values have no effect on result

    valid = []
    for a in range(8):
        for c in range(8):
            bits = check_c_valid(a, c)
            if bits:
                valid.append(bits)

    possible_values = {i: [] for i in range(8)}
    for d in valid:
        v = value_from_bit_dict(d)
        v = get_loop_value(v)
        possible_values[v].append(d)

    results = []
    combine(None, possible_values, prog[::-1], results)

    min_ok = None
    for r in results:
        init_a = value_from_bit_dict(r)
        out = run(init_a, prog)
        if out == prog and (min_ok is None or init_a < min_ok):
            min_ok = init_a

    return min_ok


def loader(input_path):
    with open(input_path, 'r') as puzzle:
        reg_a = int(puzzle.readline().split()[-1])
        reg_b = int(puzzle.readline().split()[-1])
        reg_c = int(puzzle.readline().split()[-1])
        puzzle.readline()
        prog_str = puzzle.readline().split()[-1]

    prog = [int(i) for i in prog_str.split(',')]
    return reg_a, reg_b, reg_c, prog


def solver(input_path, part, is_example=False):
    parsed_input = loader(input_path)

    if part == 1:
        result = solve_part1(parsed_input, is_example)
    else:
        result = solve_part2(parsed_input, is_example)

    return result


def run_examples():
    examples = (
        ('test_input', 1, '4,6,3,5,6,3,5,2,1,0'),
        # ('test_input2', 2, 117440),
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
    print(f'Solutions found in {took:.3f}s')  # 1ms

    # Regression test
    assert part1 == '1,6,3,6,5,6,5,1,7'
    assert part2 == 247839653009594


if __name__ == '__main__':
    run_examples()
    main()
