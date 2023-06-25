import abc
from threading import Thread
from typing import Any

import Pyro5.api


class AbstractRpcServer(abc.ABC):
    @abc.abstractmethod
    def register_object(self, service: Any, name: str):
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_object(name: str) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError


class RpcServer(AbstractRpcServer):
    def __init__(self):
        self.pyro_daemon: Pyro5.api.Daemon = Pyro5.api.Daemon()
        self.name_server: Any = Pyro5.api.locate_ns()

    def register_object(self, service: Any, name: str):
        uri: Pyro5.api.URI = self.pyro_daemon.register(service)
        self.name_server.register(f"sentinext.{name}", uri)

    @staticmethod
    def get_object(name: str) -> Pyro5.api.Proxy:
        return Pyro5.api.Proxy(f"PYRONAME:sentinext.{name}")

    def start(self):
        server_thread: Thread = Thread(target=self.pyro_daemon.requestLoop)
        server_thread.start()
