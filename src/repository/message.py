import abc
import uuid
from typing import Tuple, Iterator, Optional

from src.domain.message import Message
from src.libs.tuple_space import AbstractTupleSpace


class MessageAbstractRepository(abc.ABC):
    def __init__(self, tuple_space: AbstractTupleSpace):
        self._tuple_space: AbstractTupleSpace = tuple_space

    @abc.abstractmethod
    def add(self, message: Message):
        raise NotImplementedError

    @abc.abstractmethod
    def consume_all_messages_for_user(self, user_id: uuid.UUID) -> Iterator[Message]:
        raise NotImplementedError


class MessageRepository(MessageAbstractRepository):
    def add(self, message: Message):
        self._tuple_space.write(
            (
                "message",
                message.id,
                message.origin,
                message.destination,
                message.content,
            )
        )

    def consume_all_messages_for_user(self, user_id: uuid.UUID) -> Iterator[Message]:
        pattern: Tuple = ("message", uuid.UUID, uuid.UUID, user_id, str)

        while self._tuple_space.read(pattern):
            message_tuple: Optional[Tuple] = self._tuple_space.take(pattern)

            if message_tuple:
                yield Message(
                    message_id=message_tuple[1],
                    origin=message_tuple[2],
                    destination=message_tuple[3],
                    content=message_tuple[4],
                )
