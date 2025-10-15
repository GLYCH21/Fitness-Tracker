from faulthandler import is_enabled

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QMessageBox
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

import time, re
from datetime import datetime
from resource import common
from module.entry_repository import EntryRepository as EntryRepo

"""
widget imported:
overlay
"""


class Table(QTableWidget):
    service = None
    __headers = ["ID", "Date", "Activity", "Details", "Burned(.cal)"]

    def __new__(cls, parent=None):
        if cls.service is None:
            cls.service = super().__new__(cls)
        return cls.service


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(common.table_x, common.table_y, common.table_w, common.table_h)

        # state
        self.update_mode = False # use for toggling
        self.delete_mode = False # use for toggling
        self.config()
        # self.load_entries() # self no longer load when startup, profile_view will now request to load


    def config(self):
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setColumnCount(len(self.__headers))
        self.setHorizontalHeaderLabels(self.__headers)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        # listener
        self.cellClicked.connect(self.cell_clicked)

        # col size
        self.setColumnWidth(0, 25)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        for col in range(1, self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)


    #
    # EVENTS
    #
    def add_entry(self, entry: list | tuple):
        """
        - list - to send data to db
        - tuple - to append data to table
        """
        row = self.rowCount()
        self.insertRow(row)

        if type(entry) == list:
            """
            Send data to db to get new id
            Generate date
            insert date at 0 then new_id at 0
            """
            new_id = EntryRepo.add_entry(*entry)
            date = datetime.now().strftime("%Y-%m-%d")
            entry.insert(0, date)
            entry.insert(0, new_id)

        for col, item in enumerate(entry):
            item_widget = QTableWidgetItem(str(item))
            item_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, col, item_widget)


    def loadEntries(self, user_id):
        self.setRowCount(0)
        entries = EntryRepo.fetch_user_entries(user_id)
        [self.add_entry(entry) for entry in entries]
        self.delete_mode = self.update_mode = False


    def toggleCellMode(self, mode: str):

        if mode.lower() == "update" and not self.delete_mode:
            self.update_mode = not self.update_mode
            color = QColor(228, 139, 24)
        elif mode.lower() == "delete" and not self.update_mode:
            self.delete_mode = not self.delete_mode
            color = QColor(255, 0, 0)
        else:
            self.delete_mode = self.update_mode = False


        if self.delete_mode or self.update_mode:
            # Highlight all cells
            for r in range(self.rowCount()):
                for c in range(self.columnCount()):
                    self.item(r, c).setBackground(color)
        else:
            # Reset background
            for r in range(self.rowCount()):
                for c in range(self.columnCount()):
                    self.item(r, c).setBackground(QColor(48, 48, 48))

    # LISTENER
    def cell_clicked(self, row, column):
        entry_id = int(self.item(row, 0).text())

        if self.delete_mode:
            # dialog confirmation before deletion
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete ID {entry_id}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                EntryRepo.delete_entry(entry_id)
                time.sleep(0.1)
                self.removeRow(row)

        # UPDATE
        elif self.update_mode:
            from widget.overlay import Overlay
            activity = self.item(row, 2).text()
            details = list(map(int, re.findall(r'\d+', self.item(row, 3).text())))
            Overlay.service.showEntryForm("Update", entry_id, activity, details)
