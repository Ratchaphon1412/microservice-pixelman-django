from .encrypt import Encryption


class SecurityService:
    def __init__(self):
        self.encrypt = Encryption()
