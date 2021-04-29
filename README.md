# Liquid Democracy Visualizer

### To run the code

1. Open `config.ini` and modify the `model_args` appropriately. The number of trials can also be modified by changing the `NUM_TRIALS` variable (default 10) in `main.py`.
2. Run `python3 main.py` from the root directory.
3. An `nx.html` file should be generated. Open the file in browser to view the `pyvis` visualization of the election. The visualization is dynamic: zoom in/out, move groups of nodes around, and hover over nodes to view their competence.
4. Various statistics (including average accuracy, etc.) should also be outputted in terminal.

### Sample visualizations

From left to right:
- `graph_type` = 1, `delegation_rule` = 1
- `graph_type` = 1, `delegation_rule` = 2
- `graph_type` = 2, `delegation_rule` = 1

![Graph Types](/images/graph_types.png)
