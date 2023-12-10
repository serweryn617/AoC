class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class Directory(File):
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.contents = {}
    
    def insert(self, file):
        self.contents[file.name] = file


def recursive_get(file, keys):
    if len(keys) == 1:
        return file.contents[keys[0]]
    return recursive_get(file.contents[keys[0]], keys[1:])


def calculate_dir_sizes(tree):
    dirs = tuple(filter(lambda x: isinstance(x, Directory), tree.contents.values()))

    for node in dirs:
        calculate_dir_sizes(node)

    for node in tree.contents.values():
        tree.size += node.size



def get_sizes(tree, output):
    for node in tree.contents.values():
        if isinstance(node, Directory):
            output.append(node.size)
            get_sizes(node, output)


def solver(input_path, puzzle_type: str):
    assert puzzle_type in ('most', 'free')

    cwd = ['/']
    root = Directory('root')
    root.insert(Directory('/'))

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            elements = line.strip().split()
            if elements[0] == '$':
                if elements[1] == 'cd':
                    if elements[2] == '/':
                        cwd = ['/']
                    elif elements[2] == '..':
                        cwd.pop()
                    else:
                        f = Directory(elements[2])
                        recursive_get(root, cwd).insert(f)
                        cwd.append(elements[2])
            elif elements[0] == 'dir':
                f = Directory(elements[1])
                recursive_get(root, cwd).insert(f)
            else:  # file
                f = File(elements[1], int(elements[0]))
                recursive_get(root, cwd).insert(f)

    output = []
    calculate_dir_sizes(root)
    get_sizes(root, output)

    if puzzle_type == 'most':
        return sum(filter(lambda x: x < 100000, output))
    elif puzzle_type == 'free':
        total = 70000000
        required = 30000000
        to_free = root.size + required - total
        return min(filter(lambda x: x >= to_free, output))


if __name__ == '__main__':
    expected1 = 95437
    result1 = solver('test_input', 'most')
    assert result1 == expected1, f'Example 1 failed: {result1}'

    expected2 = 24933642
    result2 = solver('test_input', 'free')
    assert result2 == expected2, f'Example 2 failed: {result2}'

    print("Examples passed")
    print("Puzzle 1 answer:", solver('input', 'most'))
    print("Puzzle 2 answer:", solver('input', 'free'))

