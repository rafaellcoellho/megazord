import abc
import enum
from typing import Dict, Callable, Any

import stomp


class Topic(enum.Enum):
    TRACKED_MESSAGES = "tracked_messages"


class AbstractMessageBroker(abc.ABC):
    @abc.abstractmethod
    def send_message_to_topic(self, topic_name: str, message: str):
        raise NotImplementedError

    @abc.abstractmethod
    def subscribe_to_topic(self, topic_name: str, callback: Callable):
        raise NotImplementedError


class StompPyListener(stomp.ConnectionListener):
    def __init__(self, connection: stomp.Connection):
        self.connection: stomp.Connection = connection
        self.callbacks: Dict[str, Callable] = {}

    def on_error(self, frame: Any):
        print(f"broker received an error {frame.body}")

    def on_disconnected(self):
        print("broker disconnected")

    def on_message(self, frame: Any):
        message: str = frame.body
        destination: str = frame.headers["destination"]

        if destination in self.callbacks:
            self.callbacks[destination](message)

    def add_callback(self, destination: str, callback: Callable):
        self.callbacks[destination] = callback


class MessageBroker(AbstractMessageBroker):
    def __init__(self):
        self._stomp_client: stomp.Connection = stomp.Connection()
        self._stomp_client.connect(username="admin", password="admin")
        self._listener: StompPyListener = StompPyListener(connection=self._stomp_client)
        self._stomp_client.set_listener(name="", listener=self._listener)

    def send_message_to_topic(self, topic_name: str, message: str):
        self._stomp_client.send(body=message, destination=f"/topic/{topic_name}")

    def subscribe_to_topic(self, topic_name: str, callback: Callable):
        destination: str = f"/topic/{topic_name}"
        self._listener.add_callback(destination=destination, callback=callback)
        self._stomp_client.subscribe(destination=destination, id="1")
