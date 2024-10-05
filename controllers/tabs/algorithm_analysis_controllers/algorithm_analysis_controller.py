from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIntValidator
from controllers.graphs.analysisGraphController import AnalysisGraphController
from imports.topology_types import TopologyTypes


class AlgorithmAnalysis(QtWidgets.QWidget):
    def __init__(self, ui_file, topology_type: TopologyTypes):
        super().__init__()
        uic.loadUi(ui_file, self)

        # Find UI components
        self.graph_layout = self.findChild(QtWidgets.QVBoxLayout, "analysis_layout")
        self.results_label = self.findChild(QtWidgets.QLabel, "results_label")
        self.number_of_nodes_et = self.findChild(QtWidgets.QLineEdit, "number_of_nodes")
        self.number_of_paths_et = self.findChild(QtWidgets.QLineEdit, "number_of_paths")
        self.create_experiment_btn = self.findChild(QtWidgets.QPushButton, "create_experiment_btn")
        self.experiments_table = self.findChild(QtWidgets.QTableWidget, "experiments_table")
        self.change_ax_to_xyz_btn = self.findChild(QtWidgets.QPushButton, "change_ax_to_xyz")
        self.change_ax_to_xy_btn = self.findChild(QtWidgets.QPushButton, "change_ax_to_xy")
        self.change_ax_to_xz_btn = self.findChild(QtWidgets.QPushButton, "change_ax_to_xz")
        self.change_ax_to_yz_btn = self.findChild(QtWidgets.QPushButton, "change_ax_to_yz")

        # Set integer validators
        int_validator = QIntValidator(3, 10000)  # Adjust the range as needed
        self.number_of_nodes_et.setValidator(int_validator)
        self.number_of_paths_et.setValidator(int_validator)

        # Connect view adjustment buttons to methods
        self.change_ax_to_xyz_btn.clicked.connect(self.ax_to_xyz)
        self.change_ax_to_xy_btn.clicked.connect(self.ax_to_xy)
        self.change_ax_to_xz_btn.clicked.connect(self.ax_to_xz)
        self.change_ax_to_yz_btn.clicked.connect(self.ax_to_yz)

        # Connect signals to slots
        self.number_of_nodes_et.textChanged.connect(self.update_create_experiment_btn_state)
        self.number_of_paths_et.textChanged.connect(self.update_create_experiment_btn_state)
        self.create_experiment_btn.clicked.connect(self.create_new_experiment)

        # Initialize the AnalysisGraphController
        self.analysis_graph_controller = AnalysisGraphController(
            self.graph_layout, topology_type, self.results_label, self.experiments_table
        )

        # Initialize button state
        self.create_experiment_btn.setEnabled(False)

    def update_create_experiment_btn_state(self):
        """Enable or disable the create_experiment_btn based on input validity."""
        if self.number_of_nodes_et.hasAcceptableInput() and self.number_of_paths_et.hasAcceptableInput():
            self.create_experiment_btn.setEnabled(True)
        else:
            self.create_experiment_btn.setEnabled(False)

    def create_new_experiment(self):
        """Create a new experiment and update the graph and table."""
        try:
            # Get the number of nodes and paths from the input fields
            number_of_nodes = int(self.number_of_nodes_et.text().strip())
            number_of_paths = int(self.number_of_paths_et.text().strip())

            # Call the method in analysis_graph_controller to create a new experiment
            self.analysis_graph_controller.create_new_experiment(number_of_nodes, number_of_paths)

            # Clear the input fields
            self.number_of_nodes_et.clear()
            self.number_of_paths_et.clear()

            # Disable the create experiment button until valid input is entered again
            self.create_experiment_btn.setEnabled(False)

        except ValueError:
            # Handle the case where conversion to int fails (should not happen due to validators)
            QtWidgets.QMessageBox.warning(
                self,
                "Input Error",
                "Please enter valid integer values for the number of nodes and paths."
            )

    def ax_to_xyz(self):
        """Adjust the graph to a 3D perspective."""
        self.analysis_graph_controller.ax_to_xyz()

    def ax_to_xy(self):
        """Adjust the graph to the XY plane."""
        self.analysis_graph_controller.ax_to_xy()

    def ax_to_xz(self):
        """Adjust the graph to the XZ plane."""
        self.analysis_graph_controller.ax_to_xz()

    def ax_to_yz(self):
        """Adjust the graph to the YZ plane."""
        self.analysis_graph_controller.ax_to_yz()
