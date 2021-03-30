from pyvis.network import Network
import networkx as nx
import os
# net = Network()

LIGHT_GREEN = '#8ee58b'
LIGHT_RED = '#ffbcbc'

class Visualization:
    def __init__(self, graph=None):
        self.graph = graph

    def show(self, size=10):
        G = nx.DiGraph()
        
        for node in self.graph.nodes:
            title = 'Competence: ' + str(node.competence)
            G.add_node(node, size=size, title=title)

        # populates the nodes and edges data structures
        nt = Network('500px', '500px', directed=True)
        nt.from_nx(G)
        if os.path.exists("nx.html"):
            os.remove("nx.html")
        nt.show('nx.html')

    def show_sample(self, size=10):
        G = nx.DiGraph()
        G.add_node(1, size=size, title='Competence: 0.33', color='green')
        G.add_node(2, size=size, title='Competence: 0.5', color=LIGHT_GREEN)
        G.add_node(3, size=size, title='Competence: 0.65', color=LIGHT_GREEN)
        G.add_edge(2, 1, weight=5)
        G.add_edge(3, 1, weight=5)
        G.add_node(4, size=size, title='Competence: 0.2', color='red')
        G.add_node(5, size=size, title='Competence: 0.2', color=LIGHT_RED)
        G.add_edge(5, 4, weight=5)

        # populates the nodes and edges data structures
        nt = Network('500px', '500px', directed=True)
        nt.from_nx(G)
        if os.path.exists("nx.html"):
            os.remove("nx.html")
        nt.show('nx.html')

# testing:
v = Visualization()
v.show_sample()