from controllers.graphs.graphController import GraphController


class OnlineGraphController(GraphController):
    def __init__(self, layout, solution_et, topology_type):
        super(OnlineGraphController, self).__init__(layout, solution_et, topology_type)

    def _init_solution_ET(self):
        self.solution_ET.setPlainText("")

    def _update_solution_display(self, path, color):
        self.solution_ET.setPlainText(
            f"Paths= {self.algorithm.paths}"
            f"\nThe solution is {self.algorithm.solution()}"
            f"\ntotal ADMs= {sum(self.algorithm.adm)} ")
