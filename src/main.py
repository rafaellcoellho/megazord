import tkinter

if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("Sentinext")
    window.geometry("100x50")
    window.resizable(False, False)

    label = tkinter.Label(window, text="Sentinext")
    label.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.NSEW)

    window.mainloop()
