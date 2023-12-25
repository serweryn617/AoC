from copy import deepcopy


class Node:
    def __init__(self, connections):
        self.connections = list(connections)

    def add_connections(self, connections):
        for c in connections:
            if c not in self.connections:
                self.connections.append(c)

    def remove_connection(self, connection):
        if connection not in self.connections:
            return

        idx = self.connections.index(connection)
        self.connections.pop(idx)


class Pathfinder:
    def __init__(self, node, visited = (), length = 0):
        self.node = node
        self.visited = visited
        self.length = length

    def next_nodes(self, graph, max_len):
        connected = []

        for c in graph[self.node].connections:
            if c not in self.visited and self.length < max_len:
                connected.append(Pathfinder(c, self.visited + (self.node,), self.length + 1))

        return connected


def get_shortest_path(start_node, end_node, graph):
    print('get_shortest_path', start_node, end_node)
    # DFS
    length = get_shortest_path_length(start_node, end_node, graph)

    if length is None:
        return None

    heads = [Pathfinder(start_node)]

    while heads:
        head = heads.pop(0)
        if head.node == end_node:
            return head.visited + (end_node,)

        # if end_node in [h.node for h in heads]:
        #     idx = [h.node for h in heads].index(end_node)
        #     return heads[idx].visited + (end_node,)
        # head = heads.pop(0)

        # heads += head.next_nodes(graph, 1000)
        heads = head.next_nodes(graph, length + 2) + heads

    return None


def get_shortest_path_length(start_node, end_node, graph):
    print('get_shortest_path_length', start_node, end_node)
    # fill algorithm
    visited = []
    frontier = [start_node]
    length = 0

    while frontier:
        if end_node in frontier:
            return length

        length += 1
        next_nodes = []

        for f in frontier:
            for n in graph[f].connections:
                if n not in visited and n not in frontier:
                    next_nodes.append(n)

        visited += frontier
        frontier = next_nodes

    return None


def remove_edges(graph, node_list):
    for i in range(len(node_list) - 1):
        node_a = node_list[i]
        node_b = node_list[i + 1]

        graph[node_a].remove_connection(node_b)
        graph[node_b].remove_connection(node_a)


def get_number_of_paths(start_node, end_node, graph, limit = 4):
    print('get_number_of_paths')

    local_graph = deepcopy(graph)

    for num_paths in range(1, limit + 1):
        visited = get_shortest_path(start_node, end_node, local_graph)
        
        if visited is None:
            num_paths -= 1
            break

        remove_edges(local_graph, visited)

    return num_paths


def find_num_connections(graph):
    # variation of max flow algorithm
    keys = list(graph.keys())
    start_node = keys.pop(0)

    group_size = 0
    for n, end_node in enumerate(keys):
        num_paths = get_number_of_paths(start_node, end_node, graph)
        if num_paths == 3:
            group_size += 1

    return group_size


def display_graph(graph):
    print('GRAPH')
    for k, v in graph.items():
        print(k, ':', v.connections)
    print('END GRAPH')


def display_num_edges(graph):
    num_edges = sum([len(n.connections) for n in graph.values()])
    print('Num edges:', num_edges // 2)


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

    # l = get_shortest_path_length('jqt', 'rsh', graph)
    # print(l)
    # return

    total_size = len(graph)
    group_size = find_num_connections(graph)

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
    print(f'Solution found in {took:.3f}s')  # 26ms

    # Regression test
    assert part1 == 16589
    # assert part2 == 


if __name__ == '__main__':
    run_examples()
    # main()

    import cProfile
    cProfile.run("solver('input', '2d')")