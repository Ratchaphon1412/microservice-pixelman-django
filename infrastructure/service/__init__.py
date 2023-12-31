from .security import SecurityService


class Facade:
    def __init__(self):
        self.security = SecurityService()
