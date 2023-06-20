import uuid
from typing import Optional


class User:
    def __init__(self, user_id: Optional[uuid.UUID] = None, name: str = ""):
        self.id: uuid.UUID = user_id if user_id else uuid.uuid4()
        self.name: str = name

    def __eq__(self, other):
        return self.id == other.id
