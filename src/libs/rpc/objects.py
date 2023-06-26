import abc

import Pyro5.api

from src.libs.message_broker import AbstractMessageBroker, Topic


class AbstractRpcObject(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get():
        raise NotImplementedError


class AbstractCensor(AbstractRpcObject, abc.ABC):
    @abc.abstractmethod
    def submit_for_review(
        self, message: str, user_origin_name: str, user_destination_name: str
    ):
        raise NotImplementedError


@Pyro5.api.expose
class Censor(AbstractCensor):
    def __init__(self, message_broker: AbstractMessageBroker):
        self.message_broker: AbstractMessageBroker = message_broker

    def submit_for_review(
        self, message: str, user_origin_name: str, user_destination_name: str
    ):
        self.message_broker.send_message_to_topic(
            topic_name=Topic.TRACKED_MESSAGES.value,
            message=f"{user_origin_name} send to {user_destination_name} -> {message}",
        )

    @staticmethod
    def get() -> "Censor":
        return Pyro5.api.Proxy("PYRONAME:sentinext.censor")  # type: ignore
