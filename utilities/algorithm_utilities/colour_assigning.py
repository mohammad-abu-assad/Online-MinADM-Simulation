from utilities.algorithm_utilities.list_manipulation import union_all


def assign_first_colour(self, path_number, starting, ending):
    """Assign the first color to the very first path."""
    colour = self.all_colours[0]
    self.colours.append(colour)
    self.colour_paths[colour] = [path_number]
    self.path_colour.append(colour)
    self.adm[starting] += 1
    self.adm[ending] += 1
    self.colour_number += 1
    return True


def assign_colour_for_cyclic_path(self, path_number, node):
    """Assign a new color for a cyclic path (path that starts and ends at the same node)."""
    if self.colour_number >= len(self.all_colours):
        return False  # No more colors available

    colour = self.all_colours[self.colour_number]
    self.colours.append(colour)
    self.colour_paths[colour] = [path_number]
    self.path_colour.append(colour)
    self.adm[node] += 1
    self.colour_number += 1
    return True


def assign_existing_colour(self, path_number, starting, ending):
    """Attempt to assign an existing color to the current path."""
    for colour in self.colours:
        if can_assign_colour(self, colour, path_number, starting, ending):
            self.path_colour.append(colour)
            self.colour_paths[colour].append(path_number)
            return True
    return False


def can_assign_colour(self, colour, path_number, starting, ending):
    """Check if the given colour can be assigned to the current path."""
    paths_with_same_colour = self.colour_paths[colour]
    conflicts = set(self.conflict_graph.edges())

    for p in paths_with_same_colour:
        if (path_number, p) in conflicts or (p, path_number) in conflicts:
            return False

    combined_path = union_all(self.paths, paths_with_same_colour)
    start_end_intersection = {starting, ending}.intersection({combined_path[0], combined_path[-1]})

    # Handle full or partial overlap
    if len(start_end_intersection) == 2 or can_merge_with_existing_path(self, start_end_intersection, starting,
                                                                        ending):
        return True

    return False


def can_merge_with_existing_path(self, intersection, starting, ending):
    """Check if the current path can be merged with an existing path."""
    if len(intersection) == 1:
        remaining_node = list({starting, ending} - intersection)[0]
        self.adm[remaining_node] += 1
        return True
    return False


def assign_new_colour(self, path_number, starting, ending):
    """Assign a new color to the current path."""
    if self.colour_number >= len(self.all_colours):
        return False  # No more colors available

    new_colour = self.all_colours[self.colour_number]
    self.colours.append(new_colour)
    self.colour_paths[new_colour] = [path_number]
    self.path_colour.append(new_colour)
    self.adm[starting] += 1
    self.adm[ending] += 1
    self.colour_number += 1
    return True
