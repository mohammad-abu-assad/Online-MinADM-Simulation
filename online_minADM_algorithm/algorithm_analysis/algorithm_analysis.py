import random as rnd
from online_minADM_algorithm.the_algorithm.online_minadm_algorithm import OnlineMinADMAlgorithm
from utilities.paths_generation_utilities.optimal_paths_list import PathGenerator
from imports.topology_types import TopologyTypes


class AlgorithmAnalysis:
    def __init__(self, topologyType):
        self.topology_type = topologyType
        self.optimal_algorithm = OnlineMinADMAlgorithm(topologyType)
        self.online_algorithm = OnlineMinADMAlgorithm(topologyType)
        self.number_of_paths = 0
        self.number_of_nodes = 0
        self.paths = []
        self.optimal_sol = 0
        self.online_sol = 0
        self.competitive_ratio = 0

    def start_analysis(self, number_of_nodes, number_of_paths):
        self.number_of_nodes = number_of_nodes
        self.number_of_paths = number_of_paths
        self.paths.clear()
        self.optimal_algorithm.clear_algorithm()
        self.online_algorithm.clear_algorithm()
        self.online_algorithm.create_graph(number_of_nodes)
        self.optimal_algorithm.create_graph(number_of_nodes)
        path_generator = PathGenerator(number_of_nodes, number_of_paths)
        self.paths = path_generator.generate_paths(self.topology_type)
        self.calculate_optimal_sol()
        ratio_sum = 0
        for i in range(10):
            self.calculate_random_sol()
            ratio = self.online_sol / self.optimal_sol
            ratio_sum += ratio
        avg = ratio_sum / 10
        self.competitive_ratio = avg

    def calculate_optimal_sol(self):
        self.optimal_algorithm.all_colours = list(range(1, 1001))
        for path in self.paths:
            self.optimal_algorithm.add_light_path(path)
        self.optimal_sol = sum(self.optimal_algorithm.adm)

    def calculate_random_sol(self):
        self.online_algorithm.clear_algorithm_without_graph()
        self.online_algorithm.all_colours = list(range(1, 1001))
        self.online_sol = 0
        my_list = list(self.paths)
        rnd.shuffle(my_list)
        for path in my_list:
            self.online_algorithm.add_light_path(path)
        self.online_sol = sum(self.online_algorithm.adm)


if __name__ == "__main__":
    test_path_topology = AlgorithmAnalysis(topologyType=TopologyTypes.PATH_TOPOLOGY)
    test_path_topology.start_analysis(40, 10)
    print(f"competitive ratio is {test_path_topology.competitive_ratio}")
    test_ring_topology = AlgorithmAnalysis(topologyType=TopologyTypes.RING_TOPOLOGY)
    test_ring_topology.start_analysis(40, 10)
    print(f"the optimal sol is {test_ring_topology.optimal_sol}")
    print(f"the online sol is {test_ring_topology.online_sol}")
    print(f"competitive ratio is {test_ring_topology.competitive_ratio}")
