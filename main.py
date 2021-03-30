import configparser

from model import Model
from graph import Graph

CONFIG = 'config.ini'


def main():
    # read model args from CONFIG file
    config = configparser.ConfigParser()
    config.read(CONFIG)
    model_args = config['model_args']
    model_args_dict = {}  # dict: model_arg: value
    for key, value in model_args.items():
        model_args_dict[key] = value
    model = Model(model_args_dict)

    # create graph
    graph = Graph(model)
    results = graph.get_results() # Assign Delegates, Calculate "weight" of votes, Count up total votes
    total_voters = graph.model.total_voters
    correct_votes = int(results[1])
    accuracy = 1.0 * correct_votes / total_voters
    print("correct votes: " + str(correct_votes))
    print("total votes: " + str(total_voters))
    print("ACCURACY: " + str(accuracy))

    
    # visualizing graph
    # vis = Visualization(graph)
    # vis.show()



if __name__ == '__main__':
    main()
