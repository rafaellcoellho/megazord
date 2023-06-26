from src.gui.mediator import MediatorGUI
from src.libs.message_broker import MessageBroker, AbstractMessageBroker
from src.libs.rpc.objects import Censor, AbstractCensor
from src.libs.rpc.server import RpcServer, AbstractRpcServer

if __name__ == "__main__":
    message_broker: AbstractMessageBroker = MessageBroker()
    services = {
        "message_broker": message_broker,
    }

    censor: AbstractCensor = Censor(message_broker=message_broker)
    rpc_server: AbstractRpcServer = RpcServer()
    rpc_server.register_object(object_name="censor", rpc_object=censor)
    rpc_server.start()

    mediator_gui: MediatorGUI = MediatorGUI(services=services)
    mediator_gui.run()
