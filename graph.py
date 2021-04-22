import numpy as np
import random
from model import Model
from node import Node
from enum import Enum


class GraphType(Enum):
    ERDOS_RENYI = 1
    PREFERENTIAL_ATTACHMENT = 2


class Graph:
    def __init__(self, model):
        self.model = model
        self.nodes = self.generate_nodes()
        self.adj_matrix = self.generate_graph(graph_type=GraphType(model.graph_type))
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

    def generate_graph(self, graph_type=GraphType.PREFERENTIAL_ATTACHMENT):
        '''
        Generates Erdos-Renyi random graph.
        TODO: generate preferential attachment graph
        '''
        if graph_type == GraphType.ERDOS_RENYI:
            adj_matrix = self._generate_erdos_renyi_graph()
        elif graph_type == GraphType.PREFERENTIAL_ATTACHMENT:
            num_nodes = len(self.nodes)
            adj_matrix = self._generate_preferential_attachment_graph(num_nodes, int(num_nodes//5))
        else:
            raise NotImplemented()

        return adj_matrix

    def _generate_erdos_renyi_graph(self):
        nodes = self.nodes
        connect_probability = self.model.connect_probability
        adj_matrix = [[-1 for _ in range(len(nodes))] for _ in range(len(nodes))]
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if i == j:
                    adj_matrix[i][j] = 0
                if adj_matrix[j][i] != -1:  # undirected
                    adj_matrix[i][j] = adj_matrix[j][i]
                    if adj_matrix[i][j] == 1:
                        self.nodes[i].edges.append(self.nodes[j])
                else:
                    adj_matrix[i][j] = self._flip_coin(connect_probability)
                    if adj_matrix[i][j] == 1:
                        self.nodes[i].edges.append(self.nodes[j])

        return adj_matrix

    def _random_subset_with_weights(self, weights, m):
        mapped_weights = [
            (random.expovariate(w), i)
            for i, w in enumerate(weights)
        ]
        return { i for _, i in sorted(mapped_weights)[:m] }

    def _generate_preferential_attachment_graph(self, n, m):
        '''
        using barabasi-albert model
        https://stackoverflow.com/questions/59003405/barab%C3%A1si-albert-model-in-python
        n = number of nodes in final graph
        m = initial number of nodes that are fully connected / 'popular'
        '''

        # initialise with a complete graph on m vertices
        neighbors = [ set(range(m)) - {i} for i in range(m) ]
        degrees = [ m-1 for i in range(m) ]

        for i in range(m, n):
            n_neighbors = self._random_subset_with_weights(degrees, m)

            # add node with back-edges
            neighbors.append(n_neighbors)
            degrees.append(m)

            # add forward-edges
            for j in n_neighbors:
                neighbors[j].add(i)
                degrees[j] += 1

        # turn in this into adj matrix
        for line in neighbors:
            print(line)

        adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(len(neighbors)):
            for neighbor in neighbors[i]:
                adj_matrix[i][neighbor] = 1
                self.nodes[i].edges.append(self.nodes[neighbor])

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

    def get_raw_results(self):
        results = {0: 0, 1: 0}
        for node in self.nodes:
            candidate = node.vote
            results[candidate] += 1
        return results

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

    def _construct_all_paths(self):
        nodes = self.nodes

        # construct reverse graph of who points to who; also find sources of the reverse graph (nodes that don't delegate their vote)
        rev_delegate_adj_matrix = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        sources = []
        for node in nodes:
            if node.delegate is not None:
                i = node.name
                j = node.delegate.name
                rev_delegate_adj_matrix[j][i] = 1
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

    def _satisfies_delegation_degree(self):
        '''
        If any node's distance from their final delegate exceeds their delegation degree,
        change their delegate to None and return False; otherwise, return True. Note that
        nodes are examined starting at the root of each path in self.all_paths.
        '''
        all_paths = self.all_paths.copy()
        for path in all_paths:
            if len(path) > 1:
                for i in range(1, len(path)):
                    if path[i][1] > path[i][0].delegation_degree:
                        path[i][0].delegate = None
                        return False
        return True

    def get_results(self):
        '''
        Return the results of the election, i.e. the number of votes
        each candidate received.
        '''
        self._assign_delegates()

        self._construct_all_paths()
        while not self._satisfies_delegation_degree():
            self._construct_all_paths()

        # tally votes
        results = {0: 0, 1: 0}
        for path in self.all_paths:
            num_votes = len(path)
            candidate = path[0][0].vote  # all votes in this path go towards `candidate`
            results[candidate] += num_votes
        return results

    def get_longest_path_len(self):
        longest_path_len = 0
        for path in self.all_paths:
            longest_path_len = max(longest_path_len, len(path))
        return longest_path_len

    def get_avg_path_len_and_sd(self):
        path_lens = []
        for path in self.all_paths:
            path_lens.append(len(path))
        return np.mean(path_lens), np.std(path_lens)

    def get_longest_dist_from_root(self):
        longest_dist = 0
        for path in self.all_paths:
            for _, dist in path:
                longest_dist = max(longest_dist, dist)
        return longest_dist
    
    def get_num_paths(self):
        return len(self.all_paths)
