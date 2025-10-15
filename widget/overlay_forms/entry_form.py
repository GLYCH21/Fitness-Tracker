
from PyQt6.QtWidgets import *

from module.entry import Entry
from resource.builder import Build
from resource import common


class EntryForm(QWidget):
    __activities: dict[str, dict] = {
        "Walking": {"type": "time", "MET": 3.9},
        "Jogging": {"type": "time", "MET": 8.0},
        "Running": {"type": "time", "MET": 9.8},
        "Jumping Rope": {"type": "time", "MET": 12.0},
        "Planking": {"type": "time", "MET": 4.0},
        "Bodyweight Squats": {"type": "reps", "MET": 5.0},
        "Lunges": {"type": "reps", "MET": 5.0},
        "Push-ups": {"type": "reps", "MET": 4.0},
        "Sit-ups": {"type": "reps", "MET": 4.0},
    }

    def __init__(self, overlay, main_window):
        super().__init__()
        self.overlay = overlay
        self.main_window = main_window
        self.current_entry_id = None  # Use when update mode
        self.setFixedSize(overlay.width(), int(overlay.height()*0.8))

        # widgets
        self.activity_dropdown = QComboBox()
        self.duration_input = Build.widget(QLineEdit, placeholder="Duration(minutes)")
        self.reps_input = Build.widget(QLineEdit, placeholder="Reps")
        self.sets_input = Build.widget(QLineEdit, placeholder="Sets")
        self.cancel_btn = QPushButton("Cancel")
        self.submit_btn = QPushButton("Submit")
        self.update_btn = QPushButton("Update")

        # LAYOUT
        self.main_layout = QVBoxLayout(self)

        self.config()

        # state
        self.reps_input.hide()
        self.sets_input.hide()
        self.update_btn.hide()
        self.hide()

    def config(self):
        self.activity_dropdown.addItems(self.__activities.keys())

        # Event Listener
        self.submit_btn.clicked.connect(self.submitEntry)
        self.update_btn.clicked.connect(self.updateEntry)
        self.cancel_btn.clicked.connect(self.overlay.hideOverlay)
        self.activity_dropdown.currentTextChanged.connect(self.toggleFields)

        # local instance
        label1 = QLabel("Activity:")
        label2 = QLabel("Details:")

        # layout container
        rep_div = Build.flex_row(self.reps_input, self.sets_input)
        btn_div = Build.flex_row(self.cancel_btn, self.submit_btn, self.update_btn)

        for el in [label1,self.activity_dropdown,label2,self.duration_input,rep_div,btn_div]:
            if isinstance(el, QLayout): self.main_layout.addLayout(el)
            else: self.main_layout.addWidget(el)

    @property
    def create_entry(self) -> Entry:
        """
        validate data inside the constructor
        """
        from widget.profile_view import ProfileView
        activity = self.activity_dropdown.currentText()
        user_info = ProfileView.service.user_info
        entry = Entry(user_info,
                      activity,
                      self.__activities[activity],
                      self.duration_input.text(),
                      self.reps_input.text(),
                      self.sets_input.text()
                      )
        return entry


    """
    EVENTS
    """
    def form(self, mode, entry_id=None, activity=None, details=None):
        """
        if mode is "create" then reset fields and buttons to prepare Add-Form
        otherwise prepare for Update-Form
        finally show the form(self)
        """
        if mode.lower() == "create":
            self.resetAll() # reset means hiding
        else:
            self.activity_dropdown.setCurrentIndex(self.activity_dropdown.findText(activity))
            self.submit_btn.hide()
            self.update_btn.show()

            self.current_entry_id = entry_id
            if len(details) > 1:
                self.reps_input.setText(str(details[0]))
                self.sets_input.setText(str(details[1]))
            else:
                self.duration_input.setText(str(details[0]))
        # Display Form
        self.show()

    def resetAll(self):
        """
        Set dropdown to default(Running) then field shown(duration) - based on activity previewed
        Clear text-fields | Buttons: show submit, hide update | Hide Overlay | Set id to None
        """
        self.activity_dropdown.setCurrentIndex(0)
        self.toggleFields()
        self.reps_input.clear()
        self.sets_input.clear()
        self.duration_input.clear()
        self.update_btn.hide()
        self.submit_btn.show()
        self.current_entry_id = None

    def toggleFields(self):
        """Change textfields base on activity type"""
        activity = self.activity_dropdown.currentText()
        activity_type = self.__activities[activity]["type"]

        if activity_type == "time":
            self.reps_input.hide()
            self.sets_input.hide()
            self.duration_input.show()
        else:
            self.duration_input.hide()
            self.reps_input.show()
            self.sets_input.show()

    def backToDefault(self):
        from widget.statusbar import StatusBar
        self.resetAll()
        self.overlay.hideOverlay()
        StatusBar.service.updateData()

    """
    ACTION EVENT
    """
    # ADD
    def submitEntry(self):
        entry = self.create_entry
        if entry.is_valid:
            from widget.table import Table
            Table.service.add_entry(entry.entry_submission + [entry.user_info["id"]])
            self.backToDefault()


    # UPDATE
    def updateEntry(self):
        entry = self.create_entry
        if entry.is_valid:
            from module.entry_repository import EntryRepository
            from widget.table import Table
            combined: list = entry.entry_submission + [self.current_entry_id]
            EntryRepository.update_entry(*combined)
            Table.service.loadEntries(entry.user_info["id"])
            self.backToDefault()