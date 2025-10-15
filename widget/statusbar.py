
from PyQt6.QtWidgets import *
from resource import common as c

class StatusBar(QStatusBar):
    service = None

    def __new__(cls, main_window):
        if cls.service is None:
            cls.service = super().__new__(cls, main_window)
        return cls.service

    def __init__(self, main_window):
        super().__init__(main_window)
        self.setGeometry(c.statusbar_x, c.statusbar_y, c.statusbar_w, c.statusbar_h)
        self.setStyleSheet("QStatusBar {background: #222;}")

        self.weight_lbl = QLabel("Weight: 20kg")
        self.calories_lbl = QLabel("Total calories burnt (today): 20kg")

        self.addWidget(self.weight_lbl)
        self.addPermanentWidget(self.calories_lbl)


    def updateWeight(self):
        from widget.profile_view import ProfileView
        weight = ProfileView.service.user_info["weight"] or 0
        self.weight_lbl.setText(f"Weight: {weight:.1f}kg")

    def updateBurntCaloriesToday(self):
        from widget.profile_view import ProfileView
        from module.entry_repository import EntryRepository
        user_id = ProfileView.service.user_info["id"]

        burnt_calories_today = EntryRepository.fetch_user_total_burnt_calories(user_id)[0] or 0

        self.calories_lbl.setText(f"Total calories burnt (today): {burnt_calories_today:.2f}")

    def updateData(self):
        self.updateWeight()
        self.updateBurntCaloriesToday()
