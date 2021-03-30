import numpy as np
import random
from model import Model
from node import Node


class Graph:
    def __init__(self, model):
        self.model = model
        self.nodes = self.generate_nodes()
        self.adj_matrix = self.generate_graph()
        self.all_paths = None

    def generate_nodes(self):
        nodes = []
        num_nodes = self.model.total_voters
        for i in range(num_nodes):
            n = Node(i, self.model)
            nodes.append(n)

        return nodes

    def _flip_coin(self, p):
        '''
        Returns 1 with probability p.
        '''
        return 1 if random.random() < p else 0

    def generate_graph(self):
        '''
        Generates Erdos-Renyi random graph.
        TODO: generate preferential attachment graph
        '''
        nodes = self.nodes
        connect_probability = self.model.connect_probability
        adj_matrix = [[-1 for _ in range(len(nodes))] for _ in range(len(nodes))]
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if i == j:
                    adj_matrix[i][j] = 0
                if adj_matrix[j][i] != -1:  # undirected
                    adj_matrix[i][j] = adj_matrix[j][i]
                    self.nodes[i].edges.append(self.nodes[j])
                else:
                    adj_matrix[i][j] = self._flip_coin(connect_probability)
                    self.nodes[i].edges.append(self.nodes[j])

        return adj_matrix

    def _assign_delegates(self):
        for node in self.nodes:
            node.assign_delegate()

    def _check_visited(self, visited, node):
        for visited_node, _ in visited:
            if node == visited_node:
                return True
        return False

    def _run_bfs(self, adj_matrix, root):
        visited = [(root, 0)]
        queue = [(root, 0)]
        while queue:
            popped_node, dist = queue.pop(0)
            for node in self.nodes:
                if adj_matrix[popped_node.name][node.name] == 1 and not self._check_visited(visited, node):
                    visited.append((node, dist + 1))
                    queue.append((node, dist + 1))
        return visited

    def _print_nodes(self):
        print('Nodes:')
        for node in self.nodes:
            print(node)

    def _print_all_paths(self):
        print('All paths:')
        i = 1
        for path in self.all_paths:
            print('Path ' + str(i) + ':')
            for node, dist in path:
                print(f"{node}, dist from root: {dist}")
            i += 1

    def get_raw_results(self):
        results = {0: 0, 1: 0}
        for node in self.nodes:
            candidate = node.vote
            results[candidate] += 1
        return results

    def get_results(self):
        '''
        Return the results of the election, i.e. the number of votes
        each candidate received.
        '''
        nodes = self.nodes
        self._assign_delegates()

        # construct reverse graph of who points to who; also find sources of the reverse graph (nodes that don't delegate their vote)
        rev_delegate_adj_matrix = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        # print('INITIAL')
        # print(rev_delegate_adj_matrix)
        sources = []
        for node in self.nodes:
            if node.delegate is not None:
                i = node.name
                j = node.delegate.name
                # print(f"edge {j},{i}")
                rev_delegate_adj_matrix[j][i] = 1
                # print(rev_delegate_adj_matrix)
            else:
                sources.append(node)

        # print('REV DELEGATE ADJ MATRIX')
        # print(rev_delegate_adj_matrix)

        # print('SOURCES')
        # for source in sources:
        #     print(source)

        # BFS from sources
        self.all_paths = []
        for root in sources:
            self.all_paths.append(self._run_bfs(rev_delegate_adj_matrix, root))

        self._print_nodes()
        self._print_all_paths()

        # tally votes
        results = {0: 0, 1: 0}
        for path in self.all_paths:
            num_votes = len(path)
            candidate = path[0][0].vote  # all votes in this path go towards `candidate`
            results[candidate] += num_votes
        return results
