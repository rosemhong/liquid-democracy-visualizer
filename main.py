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
    graph.delegate_voters()
    votes = graph.get_votes()  # calculate weight of each node and then count up votes based on weights
        # {candidate 0: weight0, candidate1: weight1}
    total_voters = graph.model.total_voters
    correct_votes = int(votes['1'])
    accuracy = 1.0 * correct_votes / total_voters
    print("ACCURACY: " + str(accuracy))
    print("correct votes: " + str(correct_votes))
    print("total votes: " + str(total_voters))
    
    # visualizing graph



if __name__ == '__main__':
    main()
