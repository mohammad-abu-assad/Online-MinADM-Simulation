from imports.topology_types import TopologyTypes
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from online_minADM_algorithm.the_algorithm.online_minadm_algorithm import OnlineMinADMAlgorithm

# Constants
NODE_SIZE = 500
CIRCULAR_LAYOUT_SCALE = 2.0
EDGE_STYLE = 'arc3,rad=0.2'


class GraphController:
    def __init__(self, layout, solution_et, topology_type):
        """Initialize the graph controller with layout, solution output, and topology type."""
        self.graph_layout = layout
        self.solution_ET = solution_et
        self.topology_type = topology_type
        self.canvas = None
        self.algorithm = OnlineMinADMAlgorithm(topology_type)  # Correct initialization
        self.ax = None

    def display_graph(self, number_of_nodes):
        """Display the graph for the given number of nodes."""
        self.algorithm.clear_algorithm()
        # Create the graph based on the topology type
        self.algorithm.create_graph(number_of_nodes)

        if hasattr(self, 'canvas') and self.canvas is not None:
            self.canvas.deleteLater()  # Properly remove the previous canvas
            plt.close(self.ax.figure)  # Close the previous figure to free resources

        # Set up the figure and canvas for the graph
        fig, ax = plt.subplots()
        ax.axis('off')
        self.ax = ax
        self.canvas = FigureCanvas(fig)

        # Draw graph based on the topology type
        if self.topology_type == TopologyTypes.PATH_TOPOLOGY:
            self._draw_path_topology(number_of_nodes)
        elif self.topology_type == TopologyTypes.RING_TOPOLOGY:
            self._draw_ring_topology(number_of_nodes)

        # Clean up the layout and add the new canvas
        self._clear_layout()
        self.graph_layout.addWidget(self.canvas)

        # Set default message in solution text box
        self._show_ETs()
        self._init_solution_ET()

    def _show_ETs(self):
        self.solution_ET.show()

    def _init_solution_ET(self):
        self.solution_ET.setPlainText("Add light paths to see results.")

    def _draw_path_topology(self, number_of_nodes):
        """Draw the path topology graph."""
        pos = {node: (node, 0) for node in self.algorithm.graph.nodes}
        nx.draw_networkx(self.algorithm.graph, ax=self.ax, pos=pos, node_size=NODE_SIZE)

    def _draw_ring_topology(self, number_of_nodes):
        """Draw the ring topology graph."""
        pos = nx.circular_layout(self.algorithm.graph, scale=CIRCULAR_LAYOUT_SCALE)

        # Draw nodes and labels
        nx.draw_networkx_nodes(self.algorithm.graph, pos=pos, ax=self.ax, node_size=NODE_SIZE)
        nx.draw_networkx_labels(self.algorithm.graph, pos, ax=self.ax)

        # Draw edges between consecutive nodes
        edges = [(i + 1, i + 2) for i in range(number_of_nodes - 1)]
        nx.draw_networkx_edges(self.algorithm.graph, edgelist=edges, pos=pos, ax=self.ax, connectionstyle=EDGE_STYLE,
                               arrows=True)

        # Draw edge to complete the ring
        nx.draw_networkx_edges(self.algorithm.graph, edgelist=[(number_of_nodes, 1)], pos=pos, ax=self.ax,
                               connectionstyle=EDGE_STYLE, arrows=True)

        self.ax.set_aspect('equal')

    def _clear_layout(self):
        """Clear the existing widgets from the layout."""
        while self.graph_layout.count():
            item = self.graph_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def add_light_path(self, path):
        """Add a new light path to the graph, plot it, and update the solution."""
        # Validate the path
        if not path or len(path) < 2:
            self.solution_ET.setPlainText("Error: Invalid path. A path must contain at least two nodes.")
            return

        # Add the path to the algorithm
        self.algorithm.add_light_path(path)
        starting_node, ending_node = path[0], path[-1]
        color = self.algorithm.path_colour[-1]

        # Get the color index
        index = self._get_color_index(color)

        # Plot based on the topology type
        if self.topology_type == TopologyTypes.PATH_TOPOLOGY:
            self._plot_path_topology(starting_node, ending_node, index, color)
        elif self.topology_type == TopologyTypes.RING_TOPOLOGY:
            self._plot_ring_topology(path, index, color)

        # Update the solution display
        self._update_solution_display(path, color)

        # Redraw the canvas and update the layout
        self.canvas.draw()
        self.graph_layout.update()

    def _get_color_index(self, color):
        """Find the index of the color in the list of assigned colors."""
        for i, col in enumerate(self.algorithm.colours):
            if col == color:
                return i
        return -1  # This should not happen if the color is valid

    def _plot_path_topology(self, starting_node, ending_node, index, color):
        """Plot the light path for path topology."""
        self.ax.plot([starting_node, ending_node - 0.1], [index + 1, index + 1], color=color)

    def _plot_ring_topology(self, path, index, color):
        """Plot the light path for ring topology."""
        # Calculate position of nodes in circular layout
        pos = nx.circular_layout(self.algorithm.graph, scale=2.5 + 0.5 * index)

        # Create edge list from the path
        edge_list = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

        # Plot the edges with the corresponding color
        nx.draw_networkx_edges(self.algorithm.graph, edgelist=edge_list, pos=pos, ax=self.ax,
                               connectionstyle=EDGE_STYLE, arrows=True, edge_color=color)

    def _update_solution_display(self, path, color):
        """Update the solution text area with the newly added path and ADM count."""
        adm_total = sum(self.algorithm.adm)
        txt = f"New path added: {path}\n" \
              f"New path's color: {color}\n" \
              f"Total ADMs: {adm_total}"
        self.solution_ET.setPlainText(txt)

    def add_light_paths(self, paths):
        """Add a set of light paths to the graph one by one."""
        if not paths:
            self.solution_ET.setPlainText("Error: No paths provided.")
            return

        # Add each path one by one
        for path in paths:
            self.add_light_path(path)

    def hide_components(self):
        if self.solution_ET:
            self.solution_ET.hide()
        self._clear_layout()
