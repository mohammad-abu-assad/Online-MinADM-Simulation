from online_minADM_algorithm.algorithm_analysis.algorithm_analysis import AlgorithmAnalysis
from experiments.experimentCounter import ExperimentCounter
from experiments.fileManager import FileManager
from imports.topology_types import TopologyTypes


class Experiment:
    def __init__(self, topology_type):
        """Initialize the Experiment class with a given topology type."""
        self.topology_type = topology_type
        topology = f"{topology_type.value}_topology"
        data_directory = f"experiments/experiments_data/{topology}/"
        results_file = f"experiments/experiments_results/{topology}/results.txt"
        counter_file = f"experiments/experiments_counters/{topology}/counter.txt"
        self.file_manager = FileManager(data_directory, results_file)
        self.counter_manager = ExperimentCounter(counter_file)
        self.algorithm_analysis = AlgorithmAnalysis(self.topology_type)

    def create_new_experiment(self, number_of_nodes, number_of_paths):
        """Creates a new experiment and stores the results."""
        if number_of_nodes < 3 or number_of_paths < 3:
            print("Number of nodes and paths must be at least 3.")
            return

        # Run the algorithm analysis
        self.algorithm_analysis.start_analysis(number_of_nodes, number_of_paths)
        counter = self.counter_manager.get_counter() + 1  # Increment counter

        # Prepare the experiment data content
        content = f"{self.topology_type.value} topology\n" \
                  f"Number of nodes: {number_of_nodes}\n" \
                  f"Number of paths: {number_of_paths}\n" \
                  f"Optimal solution: {self.algorithm_analysis.optimal_sol}\n" \
                  f"The optimal path order:\n"
        for path in self.algorithm_analysis.paths:
            content += f"{path}\n"

        # Save experiment data
        file_name = f"experiment_{counter}.txt"
        self.file_manager.save_experiment_data(file_name, content)

        # Append competitive ratio to results file
        competitive_ratio = self.algorithm_analysis.competitive_ratio
        result_line = f"{number_of_nodes},{number_of_paths},{competitive_ratio}\n"
        self.file_manager.append_to_results(result_line)

        # Update the experiment counter
        self.counter_manager.set_counter(counter)


if __name__ == "__main__":
    experiment = Experiment(TopologyTypes.RING_TOPOLOGY)
    for nodes in range(10, 101, 10):
        f = nodes // 2
        t = nodes * 2
        for paths in range(f, t + 1, 5):
            experiment.create_new_experiment(nodes, paths)
