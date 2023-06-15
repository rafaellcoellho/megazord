from src.gui.chat import ChatGUI
from src.libs.tuple_space import TupleSpace
from src.repository.message import MessageRepository
from src.repository.user import UserRepository

if __name__ == "__main__":
    tuple_space = TupleSpace()
    services = {
        "user_repository": UserRepository(tuple_space=tuple_space),
        "message_repository": MessageRepository(tuple_space=tuple_space),
    }
    chat_gui: ChatGUI = ChatGUI(services=services)
    chat_gui.run()
