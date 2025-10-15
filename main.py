"""
Project: Fitness Tracker v1.0
creator: Glicerio Tenajeros Jr.
10.11.2025 - v1.0
"""
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon

from widget.profile_view import ProfileView
from widget.toolbar import ToolBar
from widget.table import Table
from widget.overlay import Overlay
from widget.statusbar import StatusBar

from module.db import Database
from resource import common
from resource.builder import Build



class FitnessTracker(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(common.window_width, common.window_height)
        self.setWindowTitle("Fitness Tracker")
        self.setWindowIcon(QIcon('./assets/weighing-scale-64.png'))
        self.setStyleSheet(common.main_styles)

        # INSTANCES
        # db
        Database()
        # widget
        Build.widget(QLabel, object_id="title", text="Fitness Tracker", width=250, parent=self)
        self.profile_view = ProfileView(self)
        self.table = Table(self)
        self.toolbar = ToolBar(self)
        self.overlay = Overlay(self)
        self.statusbar = StatusBar(self)

        # state
        self.updateAll()

    def build_title(self):
        title = QLabel("Fitness Tracker", self)
        title.setFixedWidth(250)
        title.setObjectName("title")

    def updateAll(self):
        self.profile_view.loadUsers()
        self.profile_view.updateCurrentUserEntries()  # load the table
        self.statusbar.updateWeight()
        self.statusbar.updateBurntCaloriesToday()


if __name__ == '__main__':
    app = QApplication([])
    w = FitnessTracker()
    w.show()
    sys.exit(app.exec())