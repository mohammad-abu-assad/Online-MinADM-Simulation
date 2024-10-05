from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
import sys

from imports.custom_widgets import welcome_page


class GeneralTab(QWidget):
    def __init__(self, path_topology_tab, ring_topology_tab):
        super(GeneralTab, self).__init__()

        self.tabWidget = QTabWidget()
        self.tabWidget.setTabPosition(QTabWidget.South)

        self.tabWidget.addTab(path_topology_tab, "Path Topology")
        self.tabWidget.addTab(ring_topology_tab, "Ring Topology")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabWidget)
