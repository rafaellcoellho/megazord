import uuid
from typing import Optional, List


class Spy:
    def __init__(
        self,
        spy_id: Optional[uuid.UUID] = None,
        tracked_words: Optional[List[str]] = None,
    ):
        self.id: uuid.UUID = spy_id if spy_id else uuid.uuid4()
        self.tracked_words: List[str] = tracked_words or []

    def __eq__(self, other):
        return self.id == other.id

    def add_tracked_word(self, word: str):
        self.tracked_words.append(word)

    def remove_tracked_word(self, word: str):
        self.tracked_words.remove(word)

    def message_contains_any_tracked_word(self, message: str) -> bool:
        return any(word in message for word in self.tracked_words)
