import uuid
from typing import Optional


class Message:
    def __init__(
        self,
        origin: uuid.UUID,
        destination: uuid.UUID,
        content: str,
        message_id: Optional[uuid.UUID] = None,
    ):
        self.id: uuid.UUID = message_id if message_id else uuid.uuid4()
        self.origin: uuid.UUID = origin
        self.destination: uuid.UUID = destination
        self.content: str = content

    def __eq__(self, other):
        return self.id == other.id
