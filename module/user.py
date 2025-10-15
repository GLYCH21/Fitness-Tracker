
from resource import common

class User:
    def __init__(self, username: str, weight):
        self.username = username.capitalize()
        self.weight = common.validate_number(weight)
        self.is_valid = self.weight > 20

    @property
    def details(self) -> list:
        return [self.username, self.weight]






