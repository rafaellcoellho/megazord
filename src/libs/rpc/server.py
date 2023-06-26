import abc
from threading import Thread

import Pyro5.api

from src.libs.rpc.objects import AbstractRpcObject


class AbstractRpcServer(abc.ABC):
    @abc.abstractmethod
    def register_object(self, object_name: str, rpc_object: AbstractRpcObject):
        raise NotImplementedError

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError


class RpcServer(AbstractRpcServer):
    def __init__(self):
        self.pyro_daemon: Pyro5.api.Daemon = Pyro5.api.Daemon()
        self.name_server: Pyro5.api.Proxy = Pyro5.api.locate_ns()

    def register_object(self, object_name: str, rpc_object: AbstractRpcObject):
        uri: Pyro5.api.URI = self.pyro_daemon.register(rpc_object)
        self.name_server.register(f"sentinext.{object_name}", uri)

    def start(self):
        server_thread: Thread = Thread(target=self.pyro_daemon.requestLoop)
        server_thread.start()
