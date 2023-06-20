from typing import Optional


class CustomizeException(Exception):
    def __init__(self, status_code: int = 400, message: str = 'fail', data: Optional[dict] = None):
        self.data = data
        self.message = message
        self.status_code = status_code


class CustomizeReturn():
    def __init__(self, message: str = 'success', data: Optional[dict] = None):
        self.data = data
        self.message = message