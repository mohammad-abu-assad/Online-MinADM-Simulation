from controllers.graphs.onlineGraphController import OnlineGraphController


class OptimalGraphController(OnlineGraphController):
    def __init__(self, layout, solution_et, topology_type):
        super(OptimalGraphController, self).__init__(layout, solution_et, topology_type)

    def display_optimal_graph(self, number_of_nodes, paths):
        self.display_graph(number_of_nodes)
        self.add_light_paths(paths)

