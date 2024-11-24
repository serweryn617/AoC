EVAL_CYCLES = 20, 60, 100, 140, 180, 220


class crt:
    def __init__(self, width=40, height=6):
        self.w = width
        self.h = height
        self.x, self.y = 0, 0

    def print(self, register):
        if register - 1 <= self.x <= register + 1:
            print("#", end="")
        else:
            print(".", end="")

        self.x += 1
        if self.x == self.w:
            self.x = 0
            self.y += 1
            print()


class cpu:
    def __init__(self, register=1, eval_cycles=EVAL_CYCLES):
        self.register = register
        self.eval_cycles = eval_cycles
        self.current_cycle = 1
        self.eval_total = 0
        self.crt = crt()

    def run_instruction(self, instruction: str, args: list):
        if instruction == "noop":
            self.noop()
        if instruction == "addx":
            x = int(args[0])
            self.addx(x)
    
    def increment_cycle(self, inc_x=0):
        self.current_cycle += 1

        self.crt.print(self.register)

        self.register += inc_x
        
        if self.current_cycle in self.eval_cycles:
            self.eval_total += self.register * self.current_cycle


    def noop(self):
        self.increment_cycle()

    def addx(self, x):
        self.increment_cycle()
        self.increment_cycle(x)


def solver(input_path):
    video_cpu = cpu()

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            instruction, *args = line.strip().split()
            video_cpu.run_instruction(instruction, args)

    return video_cpu.eval_total


if __name__ == '__main__':
    expected1 = 13140
    result1 = solver('test_input')
    assert result1 == expected1, f'Example 1 failed: {result1}'

    print("Examples passed")
    print("Puzzle 1 answer:", solver('input'))

