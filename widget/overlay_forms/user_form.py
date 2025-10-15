
from PyQt6.QtWidgets import *
from resource.builder import Build
from widget.profile_view import ProfileView


class UserForm(QWidget):

    def __init__(self, overlay):
        super().__init__()
        self.overlay = overlay
        # widgets
        self.username_input = Build.widget(QLineEdit, placeholder="Name")
        self.weight_input = Build.widget(QLineEdit, placeholder="Weight(kg)")
        self.cancel_btn: QPushButton = Build.widget(QPushButton, text="Cancel")
        self.submit_btn: QPushButton = Build.widget(QPushButton, text="Submit")

        # layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.weight_input)
        self.layout.addLayout(Build.flex_row(self.cancel_btn, self.submit_btn))

        # listener
        self.submit_btn.clicked.connect(self.submit)
        self.cancel_btn.clicked.connect(self.cancel)

        # state
        self.hide()

    def showForm(self):
        self.show()


    def submit(self):
        from module.user import User
        user = User(self.username_input.text(), self.weight_input.text())

        if user.is_valid:
            from module.user_repository import UserRepository
            from widget.profile_view import ProfileView
            success: bool = UserRepository.createUser(*user.details)
            if success:
                ProfileView.service.loadUsers(user.details[0])
                ProfileView.service.updateCurrentUserEntries()
                self.overlay.hideOverlay()

    def cancel(self):
        from widget.profile_view import ProfileView
        ProfileView.service.loadUsers()
        ProfileView.service.updateCurrentUserEntries()
        self.username_input.clear()
        self.weight_input.clear()
        self.overlay.hideOverlay()




