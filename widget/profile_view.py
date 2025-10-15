
from PyQt6.QtWidgets \
import QWidget, QComboBox, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon

from module.user_repository import UserRepository
from resource.builder import Build
from resource import common


class ProfileView(QWidget):
    service = None
    Create_Profile = "Add Profile"

    def __new__(cls, main_window):
        """Ensure that only one instance is created."""
        if cls.service is None:
            cls.service = super().__new__(cls)
        return cls.service

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setGeometry(common.profile_x, common.profile_y, common.profile_w, common.profile_h)

        # widgets
        self.dropdown: QComboBox = Build.widget(QComboBox, width=int(self.width()*0.5))
        self.delete_btn: QPushButton = Build.widget(QPushButton, width=28); self.delete_btn.setIcon(QIcon("./assets/icons8-delete-96.png"))

        # layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.dropdown)
        self.layout.addWidget(self.delete_btn)

        # config
        self.connect()
        self.delete_btn.clicked.connect(self.deleteUser)





    @property
    def user_info(self) -> dict:
        """
        fetches a user info from user-table base on dropdown selected
        :return: dict that contains id, name, weight
        """
        username = self.current_username
        info = {}
        fetched = UserRepository.fetch_user_info(username)
        for x, y in zip(fetched, ["id", "name", "weight"]):
            info[y] = x
        return info

    @property
    def current_username(self) -> str:
        return self.dropdown.currentText()

    """
    EVENT
    """
    def connect(self):
        self.dropdown.currentTextChanged.connect(self.updateCurrentUserEntries)


    def loadUsers(self, username=None):
        """
        disconnect dropdown listener to avoid bug/error then turn it on after clearing items
        get usernames in db and add 'Add-profile' indicator
        if load request come from submit then display the username currently submitted
        """
        self.dropdown.currentTextChanged.disconnect()
        self.dropdown.clear()
        self.connect()
        items = UserRepository.fetch_usernames() + [self.Create_Profile]
        self.dropdown.addItems(items)
        if username:
            self.dropdown.setCurrentIndex(self.dropdown.findText(username))


    def updateCurrentUserEntries(self):
        f"""if {self.Create_Profile} is selected then reveal add-profile overlay 
        otherwise load entries(table) based on user selected"""
        if self.current_username == ProfileView.Create_Profile:
            from widget.overlay import Overlay
            Overlay.service.showUserForm()
        else:
            from widget.table import Table
            from widget.statusbar import StatusBar
            info = self.user_info
            Table.service.loadEntries(info["id"])
            StatusBar.service.updateData()


    def deleteUser(self):
        """
        Return if user trying to delete Default-data
        Delete user in db base on user_id then update dropdown users
        """
        if self.current_username in ["Default", self.Create_Profile]: return  # immediately return

        from module.user_repository import UserRepository
        user_id = self.user_info["id"]
        if user_id > -1:
            UserRepository.deleteUser(user_id)
            self.loadUsers()
            self.updateCurrentUserEntries()






