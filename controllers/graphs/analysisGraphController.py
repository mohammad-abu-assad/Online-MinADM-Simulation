from PyQt5 import QtCore
from experiments.experiment import Experiment
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from imports.topology_types import TopologyTypes


class AnalysisGraphController:
    """Controller class to manage and display the analysis graph."""

    def __init__(self, layout: QVBoxLayout, topology_type: TopologyTypes, label: QLabel, results_table: QTableWidget):
        """
        Initialize the AnalysisGraphController.

        Args:
            layout (QVBoxLayout): The layout to which the graph canvas will be added.
            topology_type (TopologyTypes): The type of topology (e.g., path or ring).
            label (QLabel): A label to display additional information (e.g., max and average ratios).
            results_table (QTableWidget): The table to display experiment results.
        """
        self.topology_type = topology_type
        self.layout = layout
        self.label = label
        self.results_table = results_table  # Store the results_table

        # Initialize the Experiment object
        self.experiment = Experiment(topology_type)

        # Initialize Matplotlib Figure and Canvas
        self.figure = Figure()
        self.ax = None  # Will hold the Axes3D object
        self.canvas = FigureCanvas(self.figure)

        # Add the canvas to the layout
        self.layout.addWidget(self.canvas)

        # Display the initial graph
        self._display_graph()

    def _display_graph(self):
        """Load experiment results and display them in a 3D scatter plot."""
        # Load results from the experiment's FileManager
        results = self.experiment.file_manager.load_results()
        if not results:
            print("No data available to display.")
            # Clear the table if no data
            self.results_table.clearContents()
            self.results_table.setRowCount(0)
            # Clear the figure
            self.figure.clear()
            self.canvas.draw()
            return

        # Extract data for plotting
        number_of_nodes, number_of_paths, competitive_ratios = self._extract_data(results)

        # Compute statistics
        max_ratio, avg_ratio = self._compute_statistics(competitive_ratios)

        # Update the label with computed statistics
        self._update_label(max_ratio, avg_ratio)

        # Map competitive ratios to colors
        colors = self._map_colors(competitive_ratios)

        # Clear the figure for fresh plotting
        self.figure.clear()

        # Create the 3D scatter plot
        self._plot_3d_scatter(number_of_nodes, number_of_paths, competitive_ratios, colors)

        # Draw the canvas
        self.canvas.draw()

        # Load results into the table
        self._load_results_to_table(number_of_nodes, number_of_paths, competitive_ratios)

    def create_new_experiment(self, number_of_nodes, number_of_paths):
        """
        Create a new experiment and update the graph.

        Args:
            number_of_nodes (int): The number of nodes in the experiment.
            number_of_paths (int): The number of paths in the experiment.
        """
        # Create a new experiment
        self.experiment.create_new_experiment(number_of_nodes, number_of_paths)

        # Update the graph with the new data
        self._display_graph()

    @staticmethod
    def _extract_data(results):
        """
        Extract data for plotting from the results.

        Args:
            results (list): List of result dictionaries.

        Returns:
            tuple: (number_of_nodes, number_of_paths, competitive_ratios)
        """
        number_of_nodes = [result['number_of_nodes'] for result in results]
        number_of_paths = [result['number_of_paths'] for result in results]
        competitive_ratios = [result['competitive_ratio'] for result in results]
        return number_of_nodes, number_of_paths, competitive_ratios

    @staticmethod
    def _compute_statistics(competitive_ratios):
        """
        Compute maximum and average competitive ratios.

        Args:
            competitive_ratios (list): List of competitive ratios.

        Returns:
            tuple: (max_ratio, avg_ratio)
        """
        max_ratio = max(competitive_ratios)
        avg_ratio = sum(competitive_ratios) / len(competitive_ratios)
        return max_ratio, avg_ratio

    def _update_label(self, max_ratio, avg_ratio):
        """
        Update the label with the max and average competitive ratios.

        Args:
            max_ratio (float): The maximum competitive ratio.
            avg_ratio (float): The average competitive ratio.
        """
        text = f"Max Ratio: {max_ratio:.2f}, Average Ratio: {avg_ratio:.2f}"
        self.label.setText(text)

    @staticmethod
    def _map_colors(competitive_ratios):
        """
        Map competitive ratios to colors for plotting.

        Args:
            competitive_ratios (list): List of competitive ratios.

        Returns:
            list: List of color strings corresponding to each competitive ratio.
        """
        colors = []
        for ratio in competitive_ratios:
            if ratio >= 1.25:
                colors.append("darkred")
            elif ratio >= 1.10:
                colors.append("red")
            else:
                colors.append("lightcoral")
        return colors

    def _plot_3d_scatter(self, x_data, y_data, z_data, colors):
        """
        Create a 3D scatter plot.

        Args:
            x_data (list): Data for the X-axis (number of nodes).
            y_data (list): Data for the Y-axis (number of paths).
            z_data (list): Data for the Z-axis (competitive ratios).
            colors (list): List of colors for the data points.
        """
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.ax.scatter(x_data, y_data, z_data, c=colors, marker='o', s=50)

        # Set labels and title
        self.ax.set_xlabel('Number of Nodes')
        self.ax.set_ylabel('Number of Paths')
        self.ax.set_zlabel('Competitive Ratio')
        self.ax.set_title(f'Algorithm Analysis for {self.topology_type.value.capitalize()} Topology')

    def _load_results_to_table(self, number_of_nodes, number_of_paths, competitive_ratios):
        """
        Load the results into the QTableWidget.

        This function clears the table and loads new data.

        Args:
            number_of_nodes (list of int): List of number of nodes.
            number_of_paths (list of int): List of number of paths.
            competitive_ratios (list of float): List of competitive ratios.
        """
        # Clear the table
        self.results_table.clearContents()
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(3)

        # Set headers
        headers = ["Nodes", "Paths", "Ratio"]
        self.results_table.setHorizontalHeaderLabels(headers)

        # Set the number of rows
        num_rows = len(number_of_nodes)
        self.results_table.setRowCount(num_rows)

        # Insert data into the table
        for i in range(num_rows):
            # Create QTableWidgetItem for each cell
            nodes_item = QTableWidgetItem(str(number_of_nodes[i]))
            paths_item = QTableWidgetItem(str(number_of_paths[i]))
            ratio_item = QTableWidgetItem(f"{competitive_ratios[i]:.2f}")

            # Align text to center
            nodes_item.setTextAlignment(QtCore.Qt.AlignCenter)
            paths_item.setTextAlignment(QtCore.Qt.AlignCenter)
            ratio_item.setTextAlignment(QtCore.Qt.AlignCenter)

            # Set the items in the table
            self.results_table.setItem(i, 0, nodes_item)
            self.results_table.setItem(i, 1, paths_item)
            self.results_table.setItem(i, 2, ratio_item)

    def ax_to_xyz(self):
        """Adjust the view to a 3D perspective."""
        if self.ax is not None:
            self.ax.view_init(elev=30, azim=-60)  # Adjust elevation and azimuth for 3D view
            self.canvas.draw()
        else:
            print("No graph to adjust.")

    def ax_to_xy(self):
        """Adjust the view to the XY plane."""
        if self.ax is not None:
            self.ax.view_init(elev=90, azim=-90)  # Elevation at 90 degrees to view XY plane
            self.canvas.draw()
        else:
            print("No graph to adjust.")

    def ax_to_xz(self):
        """Adjust the view to the XZ plane."""
        if self.ax is not None:
            self.ax.view_init(elev=0, azim=-90)  # Azimuth at -90 degrees to view XZ plane
            self.canvas.draw()
        else:
            print("No graph to adjust.")

    def ax_to_yz(self):
        """Adjust the view to the YZ plane."""
        if self.ax is not None:
            self.ax.view_init(elev=0, azim=0)  # Azimuth at 0 degrees to view YZ plane
            self.canvas.draw()
        else:
            print("No graph to adjust.")
