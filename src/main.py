from src.gui.chat import ChatGUI
from src.libs.tuple_space import TupleSpace

if __name__ == "__main__":
    services = {
        "tuple_space": TupleSpace(),
    }
    chat_gui: ChatGUI = ChatGUI(services=services)
    chat_gui.run()
