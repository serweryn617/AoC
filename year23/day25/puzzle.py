class Node:
    def __init__(self, connections):
        self.connections = list(connections)

    def add_connections(self, connections):
        for c in connections:
            if c not in self.connections:
                self.connections.append(c)


def get_connections(macro_node, graph):
    connections = {}

    for node in macro_node:
        edges = graph[node].connections
        for edge in edges:
            if edge in macro_node:
                # internal connection
                continue

            if edge in connections:
                connections[edge] += 1
            else:
                connections[edge] = 1

    return connections


def find_group_size(node, graph, expected = 3):
    # Stoer–Wagner algorithm
    macro_node = [node]

    while True:
        outside_connections = get_connections(macro_node, graph)
        min_cut = sum(outside_connections.values())

        if min_cut == expected:
            return len(macro_node)

        max_key = max(outside_connections, key = outside_connections.get)
        macro_node.append(max_key)

    return 0


def loader(input_path):
    graph = {}

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            name, connections = line.split(':')
            connections = connections.split()

            arr = [(name, connections)] + [(c, [name]) for c in connections]

            for n, con in arr:
                if n not in graph:
                    graph[n] = Node(con)
                else:
                    graph[n].add_connections(con)

    return graph


def solver(input_path, puzzle_type):
    assert puzzle_type in ('2d', 'longest')

    graph = loader(input_path)

    start_node = tuple(graph.keys())[0]

    total_size = len(graph)
    group_size = find_group_size(start_node, graph)

    return (total_size - group_size) * group_size


def run_examples():
    examples = (
        ('test_input', '2d', 54),
        # ('test_input', 'rock', (), 47),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} {puzzle_type} failed: {result}'

    print("Examples passed")


def main():
    import time
    start_time = time.time()

    part1 = solver('input', '2d')
    # part2 = solver('input', 'rock')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    # print('Puzzle 2 answer:', part2)
    print(f'Solution found in {took:.3f}s')  # 1800ms

    # Regression test
    assert part1 == 562912
    # assert part2 == 


if __name__ == '__main__':
    run_examples()
    main()
