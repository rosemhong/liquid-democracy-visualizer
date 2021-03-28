import numpy as np
import random
from model import Model

class Node:
    def __init__(self, name, model):
        self.name = name
        self.model = model
        
        self.edges = []  # social network
        self.weight = 1  # strength of vote
        self.delegate = None  # which node this node has delegated to
        self.eligible_delegates = []  # possible nodes this node can delegate to
        self.followers = []  # nodes who have delegated to this node

        # parameters:
        self.threshold = self.model.threshold_diff  # how much more competent another voter needs to be
        self.competence = self.sample_competence()  # drawn IID from N(mean, SD)
        self.vote = self.sample_vote()  # candidate that voter prefers

    def sample_competence(self):
        # return between 0 and 1 inclusive
        mean = self.model.competence_mean
        sd = self.model.competence_sd
        c = np.random.normal(mean, sd)
        if c > 1:
            c = 1
        elif c < 0:
            c = 0

        return c 
    
    def sample_vote(self):
        if self.competence > 0.5:
            v = 1  # correct candidate
        else:
            v = 0  # incorrect candidate

        return v
    
    def find_eligible_delegates(self):
        '''
        fills out self.eligible_delegates
        wildcards: error when determining who is a potential delegate
            (ie 0.8 * delegate competency)
        '''
        pass
    
    def delegate(self):
        '''
        delegate vote based on self.eligible_delegates and any delegation rules
        rules could be: pick randomly, pick most competent

        if self.eligible_delegates is empty, make weight 0
        '''
        pass
    
    def vote(self):
        '''
        vote for whoever u like most, if your vote was delegated, your weight is 0
        '''
        # return (v, weight)
        pass


class Graph:
    def __init__(self, model):
        self.model = model
        self.nodes = self.generate_nodes()
        self.adjacency_matrix = self.generate_graph()

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
        '''
        nodes = self.nodes
        connect_probability = self.model.connect_probability
        adjacency_matrix = [[None * len(nodes)] * len(nodes)]
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if i == j:
                    adjacency_matrix[i][j] = 0
                if adjacency_matrix[j][i] is not None:  # undirected
                    adjacency_matrix[i][j] = adjacency_matrix[j][i]
                    self.nodes[i].edges.append(self.nodes[j])
                else:
                    adjacency_matrix[i][j] = self._flip_coin(connect_probability)
                    self.nodes[i].edges.append(self.nodes[j])

        return adjacency_matrix

    def delegate_voters(self):
        for node in self.nodes:
            node.delegate()

    def get_votes(self):
        '''
        Return the results of the election, i.e. the number of votes
        each candidate received.
        '''
        # find sinks (nodes without a delegate)
        # bfs from sinks and count up
        pass
