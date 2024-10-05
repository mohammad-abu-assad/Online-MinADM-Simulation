from PyQt5 import QtWidgets, uic
import random as rnd
import copy
from controllers.graphs.onlineGraphController import OnlineGraphController
from controllers.graphs.optimalGraphController import OptimalGraphController
from utilities.paths_generation_utilities.optimal_paths_list import PathGenerator


class OptimalSolution(QtWidgets.QWidget):
    def __init__(self, layout, topology_type):
        super().__init__()
        uic.loadUi(layout, self)

        self.number_of_nodes_combo_box = self.findChild(QtWidgets.QComboBox, "number_of_nodes")
        self.number_of_paths_combo_box = self.findChild(QtWidgets.QComboBox, "number_of_paths")
        self.create_btn = self.findChild(QtWidgets.QPushButton, "create_btn")
        self.optimal_graph_layout = self.findChild(QtWidgets.QVBoxLayout, "optimal_graph_layout")
        self.online_graph_layout = self.findChild(QtWidgets.QVBoxLayout, "online_graph_layout")
        self.optimal_path_arrival_ET = self.findChild(QtWidgets.QPlainTextEdit, "optimal_path_arrival")
        self.online_path_arrival_ET = self.findChild(QtWidgets.QPlainTextEdit, "online_path_arrival")
        self.btn_widget = self.findChild(QtWidgets.QWidget, "btn_widget")
        self.add_path_btn = self.findChild(QtWidgets.QPushButton, "add_path_btn")
        self.add_path_btn.clicked.connect(self.add_path)
        self.add_all_paths_btn = self.findChild(QtWidgets.QPushButton, "add_all_btn")
        self.add_all_paths_btn.clicked.connect(self.add_all_paths)
        self.restart_btn = self.findChild(QtWidgets.QPushButton, "restart_btn")
        self.restart_btn.clicked.connect(self.restart_online_graph)
        self.clear_all_btn = self.findChild(QtWidgets.QPushButton, "clear_all_btn")
        self.clear_all_btn.clicked.connect(self.clear_all)

        self.online_graph_controller = OnlineGraphController(self.online_graph_layout, self.online_path_arrival_ET,
                                                             topology_type)
        self.optimal_graph_controller = OptimalGraphController(self.optimal_graph_layout, self.optimal_path_arrival_ET,
                                                               topology_type)

        self.paths_in_optimal_order = []
        self.paths_in_random_order = []
        self.topology_type = topology_type
        self.number_of_paths_combo_box.currentTextChanged.connect(self.update_create_btn_state)
        self.number_of_nodes_combo_box.currentTextChanged.connect(self.update_create_btn_state)
        self.create_btn.clicked.connect(self.create_optimal_and_online_graphs)
        self.clear()

    def clear(self):
        self.optimal_graph_controller.hide_components()
        self.online_graph_controller.hide_components()
        if self.btn_widget:
            self.btn_widget.hide()

    def reset_buttons_state(self):
        self.add_path_btn.setEnabled(True)
        self.add_all_paths_btn.setEnabled(True)
        self.restart_btn.setEnabled(False)
        self.clear_all_btn.setEnabled(True)

    def update_create_btn_state(self):
        """Enable the create button only when valid numbers of nodes and paths are selected."""
        # Get the selected text from the combo boxes
        number_of_nodes_text = self.number_of_nodes_combo_box.currentText()
        number_of_paths_text = self.number_of_paths_combo_box.currentText()

        # Ensure valid selections are made
        if number_of_nodes_text == "Number of nodes" or number_of_paths_text == "Number of paths":
            self.create_btn.setEnabled(False)
        else:
            self.create_btn.setEnabled(True)

    def create_optimal_and_online_graphs(self):
        """Create the graphs when the create button is clicked."""
        # Get the number of nodes and paths from the combo boxes
        try:
            number_of_nodes = int(self.number_of_nodes_combo_box.currentText())
            number_of_paths = int(self.number_of_paths_combo_box.currentText())
        except ValueError:
            self.optimal_path_arrival_ET.setPlainText("Error: Please select valid numbers for nodes and paths.")
            return
        path_generator = PathGenerator(number_of_nodes, number_of_paths)
        self.paths_in_optimal_order = path_generator.generate_paths(self.topology_type)
        self.paths_in_random_order = copy.deepcopy(self.paths_in_optimal_order)
        rnd.shuffle(self.paths_in_random_order)
        if self.paths_in_optimal_order:
            self.optimal_graph_controller.display_optimal_graph(number_of_nodes, self.paths_in_optimal_order)
            self.online_graph_controller.display_graph(number_of_nodes)
            self.reset_buttons_state()
            self.btn_widget.show()
        else:
            self.optimal_path_arrival_ET.setPlainText("Error: No paths generated.")

    def add_path(self):
        if len(self.paths_in_random_order) == len(self.paths_in_optimal_order):
            self.restart_btn.setEnabled(True)
        if self.paths_in_random_order:
            self.online_graph_controller.add_light_path(self.paths_in_random_order.pop(0))
            if not self.paths_in_random_order:
                self.add_path_btn.setEnabled(False)
                self.add_all_paths_btn.setEnabled(False)
                cr = sum(self.online_graph_controller.algorithm.adm) / sum(self.optimal_graph_controller.algorithm.adm)
                text = self.online_path_arrival_ET.toPlainText()
                self.online_path_arrival_ET.setPlainText(f"{text}, competitive ratio= {round(cr, 2)}")

    def add_all_paths(self):
        while self.paths_in_random_order:
            self.add_path()

    def restart_online_graph(self):
        self.paths_in_random_order = copy.deepcopy(self.paths_in_optimal_order)
        rnd.shuffle(self.paths_in_random_order)
        self.reset_buttons_state()
        number_of_nodes = int(self.number_of_nodes_combo_box.currentText())
        self.online_graph_controller.display_graph(number_of_nodes)

    def clear_all(self):
        self.optimal_graph_controller.canvas.hide()
        self.online_graph_controller.canvas.hide()
        self.online_path_arrival_ET.hide()
        self.optimal_path_arrival_ET.hide()
        self.btn_widget.hide()
        self.number_of_nodes_combo_box.setCurrentIndex(0)
        self.number_of_paths_combo_box.setCurrentIndex(0)
