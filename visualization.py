from pyvis.network import Network
import networkx as nx
import os
from model import Model
from graph import Graph

LIGHT_GREEN = '#8ee58b'
LIGHT_RED = '#ffbcbc'


class Visualization:
    def __init__(self, graph=None):
        self.graph = graph
        self.all_paths = graph.all_paths

    def show(self, size=10, weight=5):
        G = nx.DiGraph()
        node_colors = {}  # node: color string
        
        # set colors
        for path in self.all_paths:
            d = path[0][0]
            if d.vote == 1:
                c = 'green'
            else:
                c = 'red'
            node_colors[d] = c

            for node, dist in path[1:]:
                if d.vote == 1:
                    c = LIGHT_GREEN
                else:
                    c = LIGHT_RED
                node_colors[node] = c

        # add nodes
        for node in self.graph.nodes:
            title = 'Competence: %.2f' % node.competence
            G.add_node(node.name, size=size, title=title, color=node_colors[node])

        # add edges
        for node in self.graph.nodes:
            if node.delegate is not None:
                G.add_edge(node.name, node.delegate.name, weight=weight)
            else:
                pass

        # populates the nodes and edges data structures
        nt = Network('500px', '500px', directed=True)
        # nt.show_buttons()
        nt.from_nx(G)
        if os.path.exists("nx.html"):
            os.remove("nx.html")
        nt.show('nx.html')
