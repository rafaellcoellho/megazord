import abc
import uuid
from typing import Optional, Tuple, List

from src.domain.user import User
from src.libs.tuple_space import AbstractTupleSpace


class UserAbstractRepository(abc.ABC):
    def __init__(self, tuple_space: AbstractTupleSpace):
        self._tuple_space: AbstractTupleSpace = tuple_space

    @abc.abstractmethod
    def add(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_name(self, name: str) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, user_id: uuid.UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[User]:
        raise NotImplementedError


class UserRepository(UserAbstractRepository):
    def add(self, user: User):
        self._tuple_space.write(("user", user.id, user.name))

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        user_tuple: Optional[Tuple] = self._tuple_space.read(("user", user_id, str))
        return User(user_id=user_tuple[1], name=user_tuple[2]) if user_tuple else None

    def get_by_name(self, name: str) -> Optional[User]:
        user_tuple: Optional[Tuple] = self._tuple_space.read(("user", uuid.UUID, name))
        return User(user_id=user_tuple[1], name=user_tuple[2]) if user_tuple else None

    def remove(self, user_id: uuid.UUID):
        self._tuple_space.take(("user", user_id, str))

    def get_all(self) -> List[User]:
        return [
            User(user_id=user_tuple[1], name=user_tuple[2])
            for user_tuple in self._tuple_space.read_all(("user", uuid.UUID, str))
        ]
