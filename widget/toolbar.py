
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from resource import common
from resource.builder import Build
"""
widget:
table
overlay
"""

class ToolBar(QWidget):

    def __init__(self, main_window):
        super().__init__(main_window)
        self.setGeometry(common.toolbar_x, common.toolbar_y, common.toolbar_w, common.toolbar_h)


        # widgets
        self.add_btn: QPushButton = Build.widget(QPushButton, width=30)
        self.update_btn: QPushButton = Build.widget(QPushButton, width=30)
        self.delete_btn: QPushButton = Build.widget(QPushButton, width=30)

        # toLayout
        self.mainLayout: QHBoxLayout = Build.flex_row(self.add_btn, "stretch", self.update_btn,self.delete_btn)
        self.setLayout(self.mainLayout)

        # configs
        self.config_buttons()

    def config_buttons(self):
        self.add_btn.setIcon(QIcon("./assets/icons8-add-48.png"))
        self.update_btn.setIcon(QIcon("./assets/icons8-modify-48.png"))
        self.delete_btn.setIcon(QIcon("./assets/icons8-delete-96.png"))

        from widget.table import Table
        from widget.overlay import Overlay
        self.add_btn.clicked.connect(lambda: Overlay.service.showEntryForm("create"))
        self.update_btn.clicked.connect(lambda: Table.service.toggleCellMode("update"))
        self.delete_btn.clicked.connect(lambda: Table.service.toggleCellMode("delete"))
