from PyQt5 import QtWidgets, uic
import sys


# Define the callback functions before the WelcomeTab class
def on_algorithm_simulation_clicked():
    print("Algorithm Simulation clicked")


def on_algorithm_analysis_clicked():
    print("Algorithm Analysis clicked")


def on_optimal_solution_clicked():
    print("Optimal Solution clicked")


class WelcomeTab(QtWidgets.QWidget):
    def __init__(self, layout, on_algorithm_simulation_btn_clicked, on_algorithm_analysis_btn_clicked,
                 on_optimal_solution_btn_clicked):
        super().__init__()  # Updated for Python 3
        # Adjust the path as necessary for your project structure
        uic.loadUi(layout, self)

        self.algorithm_simulation_btn = self.findChild(QtWidgets.QPushButton, "algorithm_simulation_btn")
        self.algorithm_analysis_btn = self.findChild(QtWidgets.QPushButton, "algorithm_analysis_btn")
        self.optimal_solution_btn = self.findChild(QtWidgets.QPushButton, "optimal_solution_btn")

        # Connect the buttons to the callback functions
        self.algorithm_simulation_btn.clicked.connect(on_algorithm_simulation_btn_clicked)
        self.algorithm_analysis_btn.clicked.connect(on_algorithm_analysis_btn_clicked)
        self.optimal_solution_btn.clicked.connect(on_optimal_solution_btn_clicked)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = WelcomeTab(on_algorithm_simulation_clicked, on_algorithm_analysis_clicked,
                             on_optimal_solution_clicked)
    main_window.show()
    sys.exit(app.exec_())
