from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
import sys
from imports.custom_widgets import welcome_page, GeneralTab, AlgorithmSimulationPage, \
    AlgorithmAnalysisPage, OptimalSolutionPage
from imports.layouts import layouts
from imports.topology_types import TopologyTypes


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.tabWidget = QTabWidget()
        self.setWindowTitle("online-MINADM")
        self.resize(1086, 821)

        # Initialize the tabs
        welcome_tab = welcome_page(layouts.welcome_layout.value, self.on_algorithm_simulation_clicked,
                                   self.on_algorithm_analysis_clicked,
                                   self.on_optimal_solution_clicked)
        pt_widget = AlgorithmSimulationPage(layouts.algorithm_simulation_pt_layout.value, TopologyTypes.PATH_TOPOLOGY)
        rt_widget = AlgorithmSimulationPage(layouts.algorithm_simulation_rt_layout.value, TopologyTypes.RING_TOPOLOGY)
        algorithm_simulation_tab = GeneralTab(pt_widget, rt_widget)
        pt_widget = OptimalSolutionPage(layouts.optimal_solution_pt_layout.value, TopologyTypes.PATH_TOPOLOGY)
        rt_widget = OptimalSolutionPage(layouts.optimal_solution_rt_layout.value, TopologyTypes.RING_TOPOLOGY)
        optimal_solution_tab = GeneralTab(pt_widget, rt_widget)
        pt_widget = AlgorithmAnalysisPage(layouts.algorithm_analysis_layout.value, TopologyTypes.PATH_TOPOLOGY)
        rt_widget = AlgorithmAnalysisPage(layouts.algorithm_analysis_layout.value, TopologyTypes.RING_TOPOLOGY)
        algorithm_analysis_tab = GeneralTab(pt_widget, rt_widget)

        # Add tabs to the QTabWidget
        self.tabWidget.addTab(welcome_tab, "Welcome")
        self.tabWidget.addTab(algorithm_simulation_tab, "Algorithm Simulation")
        self.tabWidget.addTab(optimal_solution_tab, "Optimal Solution")
        self.tabWidget.addTab(algorithm_analysis_tab, "Algorithm Analysis")

        self.setCentralWidget(self.tabWidget)

    def on_algorithm_simulation_clicked(self):
        self.tabWidget.setCurrentIndex(1)

    def on_optimal_solution_clicked(self):
        self.tabWidget.setCurrentIndex(2)

    def on_algorithm_analysis_clicked(self):
        self.tabWidget.setCurrentIndex(3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
