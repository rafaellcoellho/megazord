import tkinter
from tkinter import ttk
from typing import Dict, List

from src.domain.message import Message
from src.domain.spy import Spy
from src.domain.user import User


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
        name_user_destination: str = self.user_selector.get()
        message_content: str = self.input_message.get()

        user_destination: User = self.services["user_repository"].get_by_name(
            name=name_user_destination
        )

        self.services["message_repository"].add(
            message=Message(
                origin=self.user.id,
                destination=user_destination.id,
                content=message_content,
            )
        )
        self.input_message.delete(0, tkinter.END)

        self.message_box.configure(state=tkinter.NORMAL)
        self.message_box.insert(
            tkinter.END, f"Você para {user_destination.name}: {message_content}\n"
        )
        self.message_box.configure(state=tkinter.DISABLED)

    def _update_available_users_to_send_message(self):
        self.friends = {
            user.name: user
            for user in self.services["user_repository"].get_all()
            if user.id != self.user.id
        }

        self.user_selector["values"] = [user.name for user in self.friends.values()]

        if self.friends:
            self.user_selector.current(0)

    def _update_messages(self):
        messages: List[Message] = self.services[
            "message_repository"
        ].consume_all_messages_for_user(user_id=self.user.id)

        self.message_box.configure(state=tkinter.NORMAL)

        for message in messages:
            user_origin: User = self.services["user_repository"].get_by_id(
                user_id=message.origin
            )
            self.message_box.insert(
                tkinter.END, f"{user_origin.name}: {message.content}\n"
            )

        self.message_box.configure(state=tkinter.DISABLED)

    def _update_state(self):
        self._update_available_users_to_send_message()
        self._update_messages()


class ManageSpyWindow(tkinter.Toplevel):
    def __init__(self, services: Dict):
        super().__init__()

        self.services: Dict = services

        self.title("Gerenciar Espião")
        self.resizable(False, False)

        self.main_frame: tkinter.LabelFrame = tkinter.LabelFrame(
            self, text="Palavras suspeitas"
        )

        self.input_tracked_word: tkinter.Entry = tkinter.Entry(
            self.main_frame,
            font=("Arial", 15),
        )
        self.button_add_tracked_word: tkinter.Button = tkinter.Button(
            self.main_frame,
            text="Adicionar",
            command=self._add_tracked_word,
        )
        self.tracked_word_list: tkinter.Listbox = tkinter.Listbox(
            self.main_frame,
        )
        self.button_remove_tracked_word: tkinter.Button = tkinter.Button(
            self.main_frame,
            text="Remover",
            command=self._remove_tracked_word,
        )

        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.input_tracked_word.grid(row=0, column=0)
        self.button_add_tracked_word.grid(row=0, column=1)
        self.tracked_word_list.grid(row=1, column=0, columnspan=2, sticky=tkinter.EW)
        self.button_remove_tracked_word.grid(
            row=2, column=0, columnspan=2, sticky=tkinter.EW
        )

        self._update_tracked_word_list()

    def _add_tracked_word(self):
        new_tracked_word: str = self.input_tracked_word.get()

        spy: Spy = self.services["spy_repository"].get()
        spy.add_tracked_word(new_tracked_word)
        self.services["spy_repository"].update(spy)

        self.input_tracked_word.delete(0, tkinter.END)
        self._update_tracked_word_list()

    def _remove_tracked_word(self):
        selected_index: int = self.tracked_word_list.curselection()
        tracked_word_to_remove: str = self.tracked_word_list.get(selected_index)

        spy: Spy = self.services["spy_repository"].get()
        spy.remove_tracked_word(tracked_word_to_remove)
        self.services["spy_repository"].update(spy)

        self._update_tracked_word_list()

    def _update_tracked_word_list(self):
        spy: Spy = self.services["spy_repository"].get()

        self.tracked_word_list.delete(0, tkinter.END)
        for tracked_word in spy.tracked_words:
            self.tracked_word_list.insert(tkinter.END, tracked_word)


class ChatGUI:
    def __init__(self, services: Dict):
        self.services: Dict = services

        self.services["spy_repository"].add(Spy())

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
        self.button_manage_spy: tkinter.Button = tkinter.Button(
            self.main_frame,
            text="Gerenciar Espião",
            command=self._open_window_manage_spy,
        )

        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.input_name_user.grid(row=0, column=0)
        self.button_add_user.grid(row=0, column=1)
        self.user_list.grid(row=1, column=0, columnspan=2, sticky=tkinter.EW)
        self.button_go_to_messages.grid(row=2, column=0, sticky=tkinter.EW)
        self.button_remove_user.grid(row=2, column=1, sticky=tkinter.EW)
        self.button_manage_spy.grid(row=3, column=0, columnspan=2, sticky=tkinter.EW)

    def _add_user(self):
        input_value: str = self.input_name_user.get()

        new_user: User = User(name=input_value)
        self.services["user_repository"].add(user=new_user)

        self.user_list.insert(tkinter.END, new_user.name)
        self.input_name_user.delete(0, tkinter.END)

    def _remove_user(self):
        selected_index: int = self.user_list.curselection()
        user_name: str = self.user_list.get(selected_index)

        user: User = self.services["user_repository"].get_by_name(name=user_name)
        self.services["user_repository"].remove(user_id=user.id)

        self.user_list.delete(selected_index)

    def _open_window_messages_user(self):
        selected_index: int = self.user_list.curselection()
        user_name: str = self.user_list.get(selected_index)

        user: User = self.services["user_repository"].get_by_name(name=user_name)

        UserMessagesWindow(services=self.services, user=user)

    def _open_window_manage_spy(self):
        ManageSpyWindow(services=self.services)

    def run(self):
        self.gui_engine.mainloop()
