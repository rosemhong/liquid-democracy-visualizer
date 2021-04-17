import configparser
import numpy as np

from model import Model
from graph import Graph
from visualization import Visualization

CONFIG = 'config.ini'
NUM_TRIALS = 5

'''
TODO:

hard
- splitting vote among multiple delegates equally? (topo sort)

later
- run simulations by varying a parameter and holding rest constant
    - look at average accuracy + correct elections
        - compare to direct democracy

    - simple ones (ignore weight limit + delegation degree)
        - varying total voters
        - varying competence mean and sd
        - varying connect probability for graph type 1
        - varying threshold diff



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

    num_paths = []
    path_lengths = []
    path_sds = []
    max_path_lengths = []

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
        
        # get path stats
        num_paths.append(graph.get_num_paths())
        path_lengths.append(graph.get_avg_path_len_and_sd()[0])
        path_sds.append(graph.get_avg_path_len_and_sd()[1])
        max_path_lengths.append(graph.get_longest_path_len())


    # visualize graph of last loop
    vis = Visualization(graph)
    vis.show()

    # print trial results
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

    avg_num_path = np.mean(num_paths)
    num_path_sd = np.std(num_paths)

    avg_path_length = np.mean(path_lengths)
    path_length_sd = np.std(path_lengths)

    avg_longest_path_length = np.mean(max_path_lengths)
    longest_path_length_sd = np.std(max_path_lengths)

    print("  Average number of paths: {:.3f}".format(avg_num_path))
    print("  SD: {:.3f}".format(num_path_sd))
    print("  Average path length: {:.3f}".format(avg_path_length))
    print("  SD: {:.3f}".format(path_length_sd))
    print("  Average longest path length: {:.3f}".format(avg_longest_path_length))
    print("  SD: {:.3f}".format(longest_path_length_sd))

    dd_avg_accuracy = np.mean(dd_accuracies)
    dd_sd = np.std(dd_accuracies)
    print()
    print("Direct democracy results over {} trials:".format(NUM_TRIALS))
    print("  Average accuracy: {:.3f}".format(dd_avg_accuracy))
    print("  SD: {:.3f}".format(dd_sd))
    print("  {}/{} correct elections".format(dd_num_correct, NUM_TRIALS))

if __name__ == '__main__':
    main()
