import abc
from typing import Tuple, Optional, List

import linsimpy


class AbstractTupleSpace(abc.ABC):
    @abc.abstractmethod
    def write(self, tuple_to_write: Tuple):
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, pattern: Tuple) -> Optional[Tuple]:
        raise NotImplementedError

    @abc.abstractmethod
    def take(self, pattern: Tuple) -> Optional[Tuple]:
        raise NotImplementedError

    @abc.abstractmethod
    def read_all(self, pattern: Tuple) -> List[Tuple]:
        raise NotImplementedError


class TupleSpace(AbstractTupleSpace):
    def __init__(self):
        self._linsimpy_tuple_space = linsimpy.TupleSpaceEnvironment()

    def write(self, tuple_to_write: Tuple):
        self._linsimpy_tuple_space.out(tuple_to_write)

    def read(self, pattern: Tuple) -> Optional[Tuple]:
        try:
            return self._linsimpy_tuple_space.rdp(pattern)
        except KeyError:
            return None

    def take(self, pattern: Tuple) -> Optional[Tuple]:
        try:
            return self._linsimpy_tuple_space.inp(pattern)
        except KeyError:
            return None

    def read_all(self, pattern: Tuple) -> List[Tuple]:
        pattern_tuple_filter: linsimpy.tuplespace.TupleFilter = (
            linsimpy.tuplespace.TupleFilter(pattern)
        )
        return [
            item
            for item in self._linsimpy_tuple_space.items
            if pattern_tuple_filter(item)
        ]
