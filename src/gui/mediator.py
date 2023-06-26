import tkinter
from typing import Dict

from src.libs.message_broker import Topic


class MediatorGUI:
    def __init__(self, services: Dict):
        self.services = services

        self.services["message_broker"].subscribe_to_topic(
            topic_name=Topic.TRACKED_MESSAGES.value,
            callback=self._on_message_received,
        )

        self.gui_engine: tkinter.Tk = tkinter.Tk()

        self.gui_engine.title("Sentinext Mediator")
        self.gui_engine.resizable(False, False)

        self.main_frame: tkinter.Frame = tkinter.Frame(self.gui_engine)

        self.message_box: tkinter.Text = tkinter.Text(
            self.main_frame,
            state=tkinter.DISABLED,
        )

        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.message_box.grid(row=0, column=0, sticky=tkinter.EW)

    def _on_message_received(self, message: str):
        self.message_box.configure(state=tkinter.NORMAL)
        self.message_box.insert(tkinter.END, f"{message}\n")
        self.message_box.configure(state=tkinter.DISABLED)

    def run(self):
        self.gui_engine.mainloop()
