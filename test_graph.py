from graph import Graph, GraphType
from model import Model

model = Model({
    'total_voters': 25,
    'competence_mean': 0.5,
    'competence_sd': 0.2,
    'connect_probability': 0.3,
    'delegate_probability': 0,
    'threshold_diff': 0.1,
    'weight_limit': 0,
    'delegation_degrees': 0
})

graph = Graph(model)
graph.adj_matrix = graph.generate_graph(graph_type=GraphType.PREFERENTIAL_ATTACHMENT)