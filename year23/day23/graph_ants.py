import multiprocessing
import random


ALPHA = 1  # Pheromone exponent
BETA = 0  # Length exponent
EVAPORATION = 1

# Probability modifier for already visited tiles
VISITED = 0.1

CYCLES = 1000
ANT_GROUP = 64


class Ant:
    def __init__(self, node):
        self.node = node
        self.visited = []
        self.path_length = 0

    def set_next_node_function(self, func):
        self.get_nodes = func

    def set_length_function(self, func):
        self.get_length = func

    def set_get_pheromone_function(self, func):
        self.get_pheromone = func

    def set_end_reached_function(self, func):
        self.get_end_reached = func

    def go_to_next_node(self):
        probabilities = []
        next_nodes = self.get_nodes(self.node)

        # print('next', [n.start for n in next_nodes])

        for next_node in next_nodes:
            p = self.get_pheromone(next_node)
            l = self.get_length(next_node)
            probabilities.append(p ** ALPHA / l ** BETA)

            # Discourage crossing the same tile more than once
            if next_node in self.visited:
                probabilities[-1] *= VISITED

        rand = random.random()
        total = sum(probabilities)

        for i in range(len(probabilities)):
            probabilities[i] /= total
            if rand < sum(probabilities[0:i + 1]):
                self.path_length += self.get_length(self.node)
                self.visited.append(self.node)
                self.node = next_nodes[i]
                # print('moved to', self.node.start)
                break

    def reached_end(self):
        return self.get_end_reached(self.node)


class Colony:
    # def process_ant(self, args):
    #     ant, grid, pheromone = args
    #     while not ant.reached_end():
    #         ant.update_dir(grid, pheromone)
    #         ant.move(grid)

    #     return ant

    def set_next_node_function(self, func):
        self.get_nodes = func

    def set_length_function(self, func):
        self.get_length = func

    def set_get_pheromone_function(self, func):
        self.get_pheromone = func

    def set_end_reached_function(self, func):
        self.get_end_reached = func

    def set_add_pheromone_function(self, func):
        self.deposit_pheromone = func

    def generate_ant(self, start_node):
        ant = Ant(start_node)
        ant.set_next_node_function(self.get_nodes)
        ant.set_length_function(self.get_length)
        ant.set_get_pheromone_function(self.get_pheromone)
        ant.set_end_reached_function(self.get_end_reached)
        return ant

    def unleash_the_ants(self, start_node):
        ant_path_length = 0

        for _ in range(CYCLES):
            ants = [self.generate_ant(start_node) for _ in range(ANT_GROUP)]

            # pool = multiprocessing.Pool(32)
            # args = [(ant, grid, pheromone) for ant in ants]
            # ants = pool.map(process_ant, args)

            for i in range(ANT_GROUP):
                # print('Moving ant', i)
                for _ in range(200):
                # while not ants[i].reached_end():
                    # print('Moving ant', i)
                    ants[i].go_to_next_node()
                    if ants[i].reached_end():
                        break

                # print('ant', i, '-', ants[i].path_length)

            for ant in ants:
                if not ant.reached_end():
                    continue

                # dp = 1 / ant.path_length
                dp = ant.path_length
                for node in set(ant.visited):
                    self.deposit_pheromone(node, dp)

            # for y in range(len(pheromone)):
            #     for x in range(len(pheromone[0])):
            #         pheromone[y][x] = max(pheromone[y][x] * EVAPORATION, 1)

            longest = max([ant.path_length for ant in ants])
            ant_path_length = max(ant_path_length, longest)

        return ant_path_length
