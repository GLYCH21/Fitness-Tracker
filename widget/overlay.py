
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from module.entry import Entry
from resource.builder import Build
from resource import common
from widget.overlay_forms.entry_form import EntryForm
from widget.overlay_forms.user_form import UserForm
"""
widget imported:
profile_view
table
"""

class Overlay(QFrame):
    service = None

    def __new__(cls, parent):
        if cls.service is None:
            cls.service = super().__new__(cls)
        return cls.service


    def __init__(self, main_window: QMainWindow):
        super().__init__(main_window)
        self.current_entry_id = None # Use when update mode
        self.setGeometry(common.overlay_x, common.overlay_y, common.overlay_w, common.overlay_h)
        self.setStyleSheet(common.overlay_styles)

        # widgets
        self.title = QLabel("Overlay Label"); self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.entryForm = EntryForm(self, main_window)
        self.userForm = UserForm(self)

        # layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.entryForm)
        self.main_layout.addWidget(self.userForm)

        # state
        self.hide()

    #
    # EVENT
    #
    def showEntryForm(self, mode, entry_id=None, activity=None, details=None):
        self.show()
        self.title.setText(f"{'Create' if mode.lower() == 'create' else 'Update'} Entry")
        self.entryForm.form(mode, entry_id, activity, details)

    def showUserForm(self):
        self.show()
        self.title.setText("Create Profile")
        self.userForm.showForm()

    def hideOverlay(self):
        self.entryForm.hide()
        self.userForm.hide()
        self.hide()




    # ADD
    def submitEntry(self):
        entry = self.create_entry
        if entry.is_valid:
            from widget.table import Table
            Table.service.add_entry(entry.entry_submission + [entry.user_info["id"]])
            self.resetAll()

    # UPDATE
    def update_entry(self):
        entry = self.create_entry
        if entry.is_valid:
            from module.entry_repository import EntryRepository
            from widget.table import Table
            combined: list = entry.entry_submission + [self.current_entry_id]
            EntryRepository.update_entry(*combined)
            Table.service.loadEntries(entry.user_info["id"])
            self.resetAll()