import tkinter
from tkinter import ttk
from typing import Dict, List

from src.domain.user import User
from src.repository.user import UserRepository, UserAbstractRepository


class UserMessagesWindow(tkinter.Toplevel):
    def __init__(self, services: Dict, user: User):
        super().__init__()

        self.services: Dict = services
        self.user: User = user

        self.title(self.user.name)
        self.resizable(False, False)

        self.main_frame: tkinter.LabelFrame = tkinter.LabelFrame(self, text="Mensagens")

        self.button_update_state: tkinter.Button = tkinter.Button(
            self.main_frame,
            text="Atualizar",
            command=self._update_state,
        )
        self.message_box: tkinter.Text = tkinter.Text(
            self.main_frame,
            state=tkinter.DISABLED,
        )
        self.user_selector: ttk.Combobox = ttk.Combobox(
            self.main_frame,
            state="readonly",
            font=("Arial", 15),
        )
        self.input_message: tkinter.Entry = tkinter.Entry(
            self.main_frame,
            font=("Arial", 15),
        )
        self.button_send_message: tkinter.Button = tkinter.Button(
            self.main_frame,
            text="Enviar",
            command=self._send_message,
        )

        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=2)
        self.main_frame.grid_columnconfigure(1, weight=3)
        self.main_frame.grid_columnconfigure(2, weight=1)

        self.button_update_state.grid(row=0, column=0, columnspan=3, sticky=tkinter.EW)
        self.message_box.grid(row=1, column=0, columnspan=3, sticky=tkinter.EW)
        self.user_selector.grid(row=2, column=0, sticky=tkinter.EW)
        self.input_message.grid(row=2, column=1, sticky=tkinter.EW)
        self.button_send_message.grid(row=2, column=2, sticky=tkinter.EW)

        self._update_state()

    def _send_message(self):
        pass

    def _update_available_users_to_send_message(self):
        user_repository: UserAbstractRepository = UserRepository(
            tuple_space=self.services["tuple_space"]
        )
        users: List[User] = user_repository.get_all()

        self.user_selector["values"] = [
            user.name for user in users if user.id != self.user.id
        ]
        self.user_selector.current(0)

    def _update_state(self):
        self._update_available_users_to_send_message()


class ChatGUI:
    def __init__(self, services: Dict):
        self.services: Dict = services

        self.gui_engine: tkinter.Tk = tkinter.Tk()

        self.gui_engine.title("Sentinext Chat")
        self.gui_engine.resizable(False, False)

        self.main_frame: tkinter.LabelFrame = tkinter.LabelFrame(
            self.gui_engine, text="Usuários"
        )

        self.input_name_user: tkinter.Entry = tkinter.Entry(
            self.main_frame,
            font=("Arial", 15),
        )
        self.button_add_user: tkinter.Button = tkinter.Button(
            self.main_frame,
            text="Adicionar",
            command=self._add_user,
        )
        self.user_list: tkinter.Listbox = tkinter.Listbox(
            self.main_frame,
        )
        self.button_go_to_messages: tkinter.Button = tkinter.Button(
            self.main_frame,
            text="Mensagens",
            command=self._open_window_messages_user,
        )
        self.button_remove_user: tkinter.Button = tkinter.Button(
            self.main_frame,
            text="Remover",
            command=self._remove_user,
        )

        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.input_name_user.grid(row=0, column=0)
        self.button_add_user.grid(row=0, column=1)
        self.user_list.grid(row=1, column=0, columnspan=2, sticky=tkinter.EW)
        self.button_go_to_messages.grid(row=2, column=0, sticky=tkinter.EW)
        self.button_remove_user.grid(row=2, column=1, sticky=tkinter.EW)

    def _add_user(self):
        input_value: str = self.input_name_user.get()

        new_user: User = User(name=input_value)
        user_repository: UserAbstractRepository = UserRepository(
            tuple_space=self.services["tuple_space"]
        )
        user_repository.add(user=new_user)

        self.user_list.insert(tkinter.END, new_user.name)
        self.input_name_user.delete(0, tkinter.END)

    def _remove_user(self):
        selected_index: int = self.user_list.curselection()
        user_name: str = self.user_list.get(selected_index)

        user_repository: UserAbstractRepository = UserRepository(
            tuple_space=self.services["tuple_space"]
        )
        user: User = user_repository.get_by_name(name=user_name)
        user_repository.remove(user_id=user.id)

        self.user_list.delete(selected_index)

    def _open_window_messages_user(self):
        selected_index: int = self.user_list.curselection()
        user_name: str = self.user_list.get(selected_index)

        user_repository: UserAbstractRepository = UserRepository(
            tuple_space=self.services["tuple_space"]
        )
        user: User = user_repository.get_by_name(name=user_name)

        UserMessagesWindow(services=self.services, user=user)

    def run(self):
        self.gui_engine.mainloop()
