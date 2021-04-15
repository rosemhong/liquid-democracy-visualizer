import configparser
import numpy as np

from model import Model
from graph import Graph
from visualization import Visualization

CONFIG = 'config.ini'
NUM_TRIALS = 2

'''
TODO:

hard
- splitting vote among multiple delegates equally? (topo sort)

later
- run simulations by varying a parameter and holding rest constant
- graph results
- improve visualization (ie add distance from root, gradient, show accuracy)
- presentation
- write report
'''

def main():
    # read model args from config file
    config = configparser.ConfigParser()
    config.read(CONFIG)
    model_args = config['model_args']
    model_args_dict = {}  # dict: model_arg: value
    for key, value in model_args.items():
        model_args_dict[key] = value
    model = Model(model_args_dict)
    
    accuracies = []
    num_correct = 0

    dd_accuracies = []
    dd_num_correct = 0

    # run multiple trials of election
    for i in range(NUM_TRIALS):
        graph = Graph(model)
        
        # get liquid democracy results
        results = graph.get_results()
        correct_votes = int(results[1])
        total_votes = graph.model.total_voters

        # output liquid democracy results
        print("Liquid democracy, trial " + str(i) + ":")
        print("  Correct / total votes: " +
              str(correct_votes) + "/" + str(total_votes))

        accuracy = correct_votes / total_votes
        accuracies.append(accuracy)
        if accuracy >= 0.5:
            num_correct += 1
        print("  Accuracy: {:.3f}".format(accuracy))

        # get direct democracy results
        dd_results = graph.get_raw_results()
        dd_correct_votes = int(dd_results[1])
        dd_accuracy = dd_correct_votes / total_votes
        dd_accuracies.append(dd_accuracy)
        if dd_accuracy >= 0.5:
            dd_num_correct += 1

    # visualize graph of last loop
    vis = Visualization(graph)
    vis.show()

    avg_accuracy = np.mean(accuracies)
    sd = np.std(accuracies)
    print()
    print("Model parameters")
    print(model.__dict__)
    print()
    print("Liquid democracy results over {} trials:".format(NUM_TRIALS))
    print("  Average accuracy: {:.3f}".format(avg_accuracy))
    print("  SD: {:.3f}".format(sd))
    print("  {}/{} correct elections".format(num_correct, NUM_TRIALS))

    dd_avg_accuracy = np.mean(dd_accuracies)
    dd_sd = np.std(dd_accuracies)
    print()
    print("Direct democracy results over {} trials:".format(NUM_TRIALS))
    print("  Average accuracy: {:.3f}".format(dd_avg_accuracy))
    print("  SD: {:.3f}".format(dd_sd))
    print("  {}/{} correct elections".format(dd_num_correct, NUM_TRIALS))

if __name__ == '__main__':
    main()
