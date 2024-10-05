def add_conflict_edges_for_cyclic_path(self, path_number):
    """Add conflict edges for a cyclic path (where start and end are the same)."""
    for path in range(path_number):
        self.conflict_graph.add_edge(path_number, path)


def add_conflict_edges_for_linear_path(self, path_number, path_to_add, starting, ending):
    """Add conflict edges for a linear path."""
    reversed_path = list(reversed(path_to_add))

    for path in range(path_number):
        existing_path = self.paths[path]
        if _is_same_path(existing_path, path_to_add, reversed_path):
            self.conflict_graph.add_edge(path_number, path)
        elif _has_conflicting_endpoints(existing_path, starting, ending):
            continue
        elif _has_sufficient_intersection(existing_path, path_to_add):
            self.conflict_graph.add_edge(path_number, path)


def _is_same_path(existing_path, path_to_add, reversed_path):
    """Check if the current path is the same as the new path or its reverse."""
    return existing_path == path_to_add or existing_path == reversed_path


def _has_conflicting_endpoints(existing_path, starting, ending):
    """Check if two paths have conflicting endpoints (same start and end nodes)."""
    return len({starting, ending}.intersection({existing_path[0], existing_path[-1]})) == 2


def _has_sufficient_intersection(existing_path, path_to_add):
    """Check if two paths share enough nodes to be considered in conflict."""
    intersection = set(path_to_add).intersection(set(existing_path))
    return len(intersection) >= 2
