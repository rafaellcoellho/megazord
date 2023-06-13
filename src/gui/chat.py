import tkinter
from tkinter import ttk


class UserMessagesWindow(tkinter.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Usuário")
        self.resizable(False, False)

        self.main_frame: tkinter.LabelFrame = tkinter.LabelFrame(self, text="Mensagens")

        self.message_box: tkinter.Text = tkinter.Text(
            self.main_frame,
            state=tkinter.DISABLED,
        )
        self.user_selector: ttk.Combobox = ttk.Combobox(
            self.main_frame,
            values=["Usuario 1", "Usuario 2"],
            state="readonly",
            font=("Arial", 15),
        )
        self.user_selector.current(0)
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

        self.message_box.grid(row=0, column=0, columnspan=3, sticky=tkinter.EW)
        self.user_selector.grid(row=1, column=0, sticky=tkinter.EW)
        self.input_message.grid(row=1, column=1, sticky=tkinter.EW)
        self.button_send_message.grid(row=1, column=2, sticky=tkinter.EW)

    def _send_message(self):
        pass


class ChatGUI:
    def __init__(self):
        self.gui_engine = tkinter.Tk = tkinter.Tk()

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
        pass

    def _remove_user(self):
        pass

    def _open_window_messages_user(self):
        UserMessagesWindow()

    def run(self):
        self.gui_engine.mainloop()
