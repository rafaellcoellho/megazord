import abc
import uuid
from typing import Optional, Tuple

from src.domain.spy import Spy
from src.libs.tuple_space import AbstractTupleSpace


class AbstractSpyRepository(abc.ABC):
    def __init__(self, tuple_space: AbstractTupleSpace):
        self._tuple_space: AbstractTupleSpace = tuple_space

    @abc.abstractmethod
    def add(self, spy: Spy):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, spy: Spy):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self) -> Optional[Spy]:
        raise NotImplementedError


class SpyRepository(AbstractSpyRepository):
    def add(self, spy: Spy):
        self._tuple_space.write(("spy", spy.id, spy.tracked_words))

    def update(self, spy: Spy):
        self._tuple_space.take(("spy", spy.id, list))
        self._tuple_space.write(("spy", spy.id, spy.tracked_words))

    def get(self) -> Optional[Spy]:
        spy_tuple: Optional[Tuple] = self._tuple_space.read(("spy", uuid.UUID, list))
        return (
            Spy(spy_id=spy_tuple[1], tracked_words=spy_tuple[2]) if spy_tuple else None
        )
