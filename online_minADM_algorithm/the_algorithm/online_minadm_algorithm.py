import networkx as nx
from imports.topology_types import TopologyTypes
from imports.colours import ALL_COLOURS
from utilities.algorithm_utilities.colour_assigning import (
    assign_first_colour,
    assign_existing_colour,
    assign_colour_for_cyclic_path,
    assign_new_colour
)
from utilities.algorithm_utilities.conflict_adding import (
    add_conflict_edges_for_cyclic_path,
    add_conflict_edges_for_linear_path
)


class OnlineMinADMAlgorithm:
    def __init__(self, topology_type):
        """Initialize the algorithm with the specified topology type."""
        self.graph = nx.Graph()
        self.adm = []
        self.paths = []
        self.conflict_graph = nx.Graph()
        self.share_graph = nx.Graph()
        self.path_colour = []
        self.colour_paths = {}
        self.colours = []
        self.all_colours = ALL_COLOURS
        self.colour_number = 0
        self.topology_type = topology_type

    def clear_algorithm(self):
        """Clear the entire algorithm state, including the graph."""
        self.graph.clear()
        self.adm.clear()
        self._reset_algorithm_data()

    def clear_algorithm_without_graph(self):
        """Clear the algorithm state, excluding the graph structure, but reset ADM to zero."""
        self.adm = [0] * len(self.adm)
        self._reset_algorithm_data()

    def _reset_algorithm_data(self):
        """Helper method to reset the algorithm's internal data."""
        self.paths.clear()
        self.colour_paths.clear()
        self.conflict_graph.clear()
        self.share_graph.clear()
        self.path_colour.clear()
        self.colour_number = 0
        self.colours.clear()

    def create_graph(self, number_of_nodes):
        """Create a graph based on the topology type and number of nodes."""
        if number_of_nodes <= 0:
            raise ValueError("Number of nodes must be positive")

        if self.topology_type == TopologyTypes.PATH_TOPOLOGY:
            self.graph = nx.path_graph(number_of_nodes)
        elif self.topology_type == TopologyTypes.RING_TOPOLOGY:
            self.graph = nx.cycle_graph(number_of_nodes)
        else:
            raise ValueError("Unsupported topology type")

        self.graph = nx.relabel_nodes(self.graph, {i: i + 1 for i in range(number_of_nodes)})
        self.adm = [0] * (number_of_nodes + 1)

    def add_light_path(self, path):
        """Add a light path to the network, updating conflict graph and assigning color."""
        if not path or len(path) < 2:
            raise ValueError("Invalid path provided")

        self.paths.append(path)
        self.add_path_to_conflict_graph()
        self.assign_colour()

    def add_path_to_conflict_graph(self):
        """Add the most recently added path to the conflict graph."""
        path_number = len(self.paths) - 1
        path_to_add = self.paths[path_number]
        self.conflict_graph.add_node(path_number)

        if self.conflict_graph.number_of_nodes() == 1:
            return  # No conflicts possible with only one path

        starting, ending = path_to_add[0], path_to_add[-1]

        if starting == ending:
            add_conflict_edges_for_cyclic_path(self, path_number)
        else:
            add_conflict_edges_for_linear_path(self, path_number, path_to_add, starting, ending)

    def assign_colour(self):
        """Assign a color to the most recently added path."""
        path_number = len(self.paths) - 1
        path_to_add = self.paths[path_number]
        starting, ending = path_to_add[0], path_to_add[-1]

        if len(self.paths) == 1:
            return assign_first_colour(self, path_number, starting, ending)

        if starting == ending:
            return assign_colour_for_cyclic_path(self, path_number, starting)

        if assign_existing_colour(self, path_number, starting, ending):
            return True

        return assign_new_colour(self, path_number, starting, ending)

    def solution(self):
        """Return the solution as a list of tuples, each representing the paths of a specific color."""
        return [tuple(self.colour_paths[colour]) for colour in self.colours]


if __name__ == "__main__":
    test_ring_topology = OnlineMinADMAlgorithm(TopologyTypes.RING_TOPOLOGY)
    test_ring_topology.create_graph(5)
    print("\n\nring topology test: ")
    print("the input is cycle graph with 5 node (1 - 5)")
    paths = [[1, 2, 3], [3, 4], [4, 5], [5, 1], [1, 2, 3, 4, 5], [5, 1], [1, 2], [2, 3], [3, 4, 5], [5, 1]]
    for i in range(len(paths)):
        print(f"path {i} arrived: {paths[i]}")
        test_ring_topology.add_light_path(paths[i])
        print(f"path colour = {test_ring_topology.path_colour[i]}")
        print(f"ADM after adding the path: {test_ring_topology.adm}")
        print(test_ring_topology.paths)
    print(f"the solution is : {test_ring_topology.solution()}")
    print(f"total ADMs= {sum(test_ring_topology.adm)} ADMs")
