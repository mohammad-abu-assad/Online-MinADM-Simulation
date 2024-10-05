from PyQt5 import QtWidgets, uic
from imports.topology_types import TopologyTypes
from controllers.graphs.graphController import GraphController


class AlgorithmSimulation(QtWidgets.QWidget):
    def __init__(self, layout, path_or_ring):
        super().__init__()
        uic.loadUi(layout, self)

        # Find UI elements
        self.add_light_path_widget = self.findChild(QtWidgets.QWidget, "add_light_path_Widget")
        self.starting_node = self.findChild(QtWidgets.QComboBox, "starting_node")
        self.ending_node = self.findChild(QtWidgets.QComboBox, "ending_node")
        self.add_path = self.findChild(QtWidgets.QPushButton, "add_path")
        self.select_number_of_nodes = self.findChild(QtWidgets.QComboBox, "select_number_of_nodes")
        self.graph_layout = self.findChild(QtWidgets.QVBoxLayout, "graph_layout")
        self.info_txt = self.findChild(QtWidgets.QPlainTextEdit, "info_txt")
        self.number_of_nodes = 0
        self.topology_type = path_or_ring

        # Add checkbox if the topology is RING_TOPOLOGY
        if path_or_ring == TopologyTypes.RING_TOPOLOGY:
            self.is_clockwise = self.findChild(QtWidgets.QCheckBox, "is_clockwise")
            self.is_clockwise.setChecked(False)

        # Connect the signal to handle node selection
        self.select_number_of_nodes.currentTextChanged.connect(self.on_select_number_of_nodes)
        self.starting_node.currentTextChanged.connect(self.on_select_starting_node)  # Fixed typo
        self.ending_node.currentTextChanged.connect(self.on_select_ending_node)
        self.add_path.clicked.connect(self.add_light_path)

        # Initialize the graph controller
        self.graph_controller = GraphController(self.graph_layout, self.info_txt, path_or_ring)

        # Reset the interface
        self.reset()

    def reset(self):
        """Reset the UI, hiding widgets and clearing layouts."""
        self.graph_controller.hide_components()
        if self.add_light_path_widget:
            self.add_light_path_widget.hide()

    def on_select_number_of_nodes(self):
        """Handle number of nodes selection and update UI accordingly."""
        # Disable controls at the start
        self.ending_node.setEnabled(False)
        self.add_path.setEnabled(False)
        self.starting_node.clear()
        self.starting_node.addItem("starting node")

        selected_text = self.select_number_of_nodes.currentText()

        # If "number of nodes" is selected, hide widgets and reset the graph
        if selected_text == "number of nodes":
            self.add_light_path_widget.hide()
            if self.graph_controller.canvas:
                self.graph_controller.canvas.hide()
            self.info_txt.hide()
            return

        # Show the add light path widget and display graph
        self.add_light_path_widget.show()

        # Convert the selected node count to an integer
        try:
            selected_nodes = int(selected_text)
            self.number_of_nodes = selected_nodes
        except ValueError:
            self.info_txt.setPlainText("Error: Please select a valid number of nodes.")
            return

        # Display the graph for the selected number of nodes
        self.graph_controller.display_graph(selected_nodes)

        # Populate starting and ending nodes
        node_items = [str(i) for i in range(1, selected_nodes + 1)]
        self.starting_node.addItems(node_items)

    def on_select_starting_node(self):
        """Handle the selection of the starting node and update the ending node options."""
        self.add_path.setEnabled(False)
        self.ending_node.clear()
        self.ending_node.addItem("ending node")

        if self.starting_node.currentText() in ["", "starting node"]:
            self.ending_node.setEnabled(False)
            return

        self.ending_node.setEnabled(True)
        selected_start = self.starting_node.currentText()  # Keep selected_start as a string

        # Populate the ending node choices with all nodes
        node_items = [str(i) for i in range(1, self.number_of_nodes + 1)]

        # In path topology, remove the selected starting node from ending node choices
        if self.topology_type == TopologyTypes.PATH_TOPOLOGY:
            node_items.remove(selected_start)

        # Add the node items to the ending node dropdown
        self.ending_node.addItems(node_items)

    def on_select_ending_node(self):
        """Handle the selection of the ending node and update controls."""
        if self.ending_node.currentText() in ["", "ending node"]:
            self.add_path.setEnabled(False)
            if hasattr(self, 'is_clockwise'):
                self.is_clockwise.setEnabled(False)
                self.is_clockwise.setChecked(False)
            return

        # Enable the add_path button once a valid ending node is selected
        self.add_path.setEnabled(True)

        # Enable is_clockwise checkbox for ring topology
        if hasattr(self, 'is_clockwise'):
            self.is_clockwise.setEnabled(True)

    def get_path_for_path_topology(self, starting_node, ending_node):
        if starting_node > ending_node:
            starting_node, ending_node = ending_node, starting_node
        path = list(range(starting_node, ending_node + 1))
        return path

    def get_path_for_ring_topology(self, starting_node, ending_node):
        if self.is_clockwise.isChecked():
            starting_node, ending_node = ending_node, starting_node
        path = self.list_in_counter_clockwise_order(starting_node, ending_node)
        return path

    def list_in_counter_clockwise_order(self, start, end):
        number_of_nodes = self.number_of_nodes
        if start < end:
            clockwise_list = list(range(start, end + 1))
        else:
            clockwise_list = list(range(start, number_of_nodes + 1)) + list(range(1, end + 1))
        return clockwise_list

    def add_light_path(self):
        start_node = int(self.starting_node.currentText())
        end_node = int(self.ending_node.currentText())
        path = []
        if self.topology_type == TopologyTypes.PATH_TOPOLOGY:
            path = self.get_path_for_path_topology(start_node, end_node)
        else:
            path = self.get_path_for_ring_topology(start_node, end_node)
        self.graph_controller.add_light_path(path)
