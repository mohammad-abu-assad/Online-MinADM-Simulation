import random as rnd
from imports.topology_types import TopologyTypes


class PathGenerator:
    def __init__(self, number_of_nodes, number_of_paths):
        self.number_of_nodes = number_of_nodes
        self.number_of_paths = number_of_paths
        self.paths = []

    def generate_paths(self, topology_type):
        """Generate paths for either path or ring topology."""
        if self.number_of_nodes < 3 or self.number_of_paths < 3:
            return []

        paths_generated = 0  # Track total number of paths generated

        while paths_generated < self.number_of_paths:
            # Ensure we don't overshoot the required number of paths
            remaining_paths = self.number_of_paths - paths_generated

            # Generate a single path case if it's the last path
            if remaining_paths == 1:
                self._generate_single_path(topology_type)
                paths_generated += 1
                continue

            # Get the number of paths with the same color, but limit it to remaining paths
            paths_with_same_color = min(
                self._get_random_paths_with_same_color(topology_type), remaining_paths
            )

            temp = paths_with_same_color
            nodes_left = self.number_of_nodes if topology_type == TopologyTypes.PATH_TOPOLOGY else self.number_of_nodes + 1
            k = 1

            while k <= self.number_of_nodes and temp > 0:
                step = self._calculate_step(nodes_left, temp)
                self._create_path_segment(k, step, topology_type)
                k += step
                nodes_left -= step
                temp -= 1

            paths_generated += paths_with_same_color  # Update the count of generated paths

        return self.paths

    def _generate_single_path(self, topology_type):
        """Generate a single path covering all nodes."""
        if topology_type == TopologyTypes.PATH_TOPOLOGY:  # Path topology
            path = list(range(1, self.number_of_nodes + 1))
        else:  # Ring topology
            path = list(range(1, self.number_of_nodes + 1)) + [1]
        self.paths.append(path)

    def _create_path_segment(self, start, step, topology_type):
        """Create a path segment for the current topology."""
        if topology_type == TopologyTypes.PATH_TOPOLOGY:  # Path topology
            path = list(range(start, start + step + 1))
        else:  # Ring topology
            if start + step > self.number_of_nodes:
                path = list(range(start, self.number_of_nodes + 1)) + [1]
            else:
                path = list(range(start, start + step + 1))
        self.paths.append(path)

    def _calculate_step(self, nodes_left, paths_left):
        """Calculate the maximum allowable step size."""
        max_step = nodes_left - paths_left
        if paths_left == 1 or max_step <= 1:
            return max_step
        return rnd.randint(1, max_step)

    def _get_random_paths_with_same_color(self, topology_type):
        """Determine how many paths share the same color."""
        if topology_type == TopologyTypes.PATH_TOPOLOGY:
            return self._get_random_number(self.number_of_nodes, self.number_of_paths)
        return self._get_random_number_for_ring(self.number_of_nodes, self.number_of_paths)

    def _get_random_number(self, number_of_nodes, number_of_paths):
        """Get a random number of paths for path topology."""
        if number_of_paths == 2:
            return 2
        if number_of_paths < number_of_nodes:
            return rnd.randint(2, number_of_paths)
        return rnd.randint(2, number_of_nodes - 1)

    def _get_random_number_for_ring(self, number_of_nodes, number_of_paths):
        """Get a random number of paths for ring topology."""
        if number_of_paths == 2:
            return 2
        if number_of_paths < number_of_nodes:
            return rnd.randint(2, number_of_paths)
        return rnd.randint(2, number_of_nodes)
