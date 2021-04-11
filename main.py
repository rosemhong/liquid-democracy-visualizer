import configparser
import numpy as np

from model import Model
from graph import Graph
from visualization import Visualization

CONFIG = 'config.ini'
NUM_TRIALS = 5

'''
TODO:
for the next time we meet (after 4/11):
- test the functions we each wrote last time!

easy
- compare to if no one delegates (tally up direct democracy vote) - this is done in get_raw_results, just print it out in main at some point
- print parameters in main

medium
- limit number of votes for a delegate (weight_limit parameter) - eric
    - keep track of capacity
    - in find_eligible_delegates, if neighbor at capacity (goin in order), skip them
- preferential attachment graph (from Ariel's suggestion) - rachel
    - no longer symmetric
    - few popular nodes (lots of incoming edges)
- keep track of delegation degrees for each voter (delegation_degrees) - rose
    - dist in all_paths, if dist > degree for a voter, just vote themselves

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

    # run multiple trials of election
    for i in range(NUM_TRIALS):
        graph = Graph(model)
        results = graph.get_results()

        correct_votes = int(results[1])
        total_votes = graph.model.total_voters

        # output results
        print("Trial " + str(i) + ":")
        print("  Correct / total votes: " +
              str(correct_votes) + "/" + str(total_votes))

        accuracy = correct_votes / total_votes
        accuracies.append(accuracy)
        if accuracy >= 0.5:
            num_correct += 1
        print("  Accuracy: {:.3f}".format(accuracy))

    # visualize graph of last loop
    vis = Visualization(graph)
    vis.show()

    avg_accuracy = np.mean(accuracies)
    sd = np.std(accuracies)
    print()
    print("Summary over {} trials:".format(NUM_TRIALS))
    print("  Average accuracy: {:.3f}".format(avg_accuracy))
    print("  SD: {:.3f}".format(sd))
    print("  {}/{} correct elections".format(num_correct, NUM_TRIALS))

if __name__ == '__main__':
    main()
