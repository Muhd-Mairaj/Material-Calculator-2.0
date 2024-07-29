import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Material Calculator")
        self.geometry("400x300")

        self._create_widgets()


    def _create_widgets(self):
        # Create a notebook (tab control)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Create frames for each tab
        self.frame1 = ttk.Frame(self.notebook)
        self.frame2 = ttk.Frame(self.notebook)

        # Add frames to the notebook
        self.notebook.add(self.frame1, text="Enter Values")
        self.notebook.add(self.frame2, text="Excel File")

        # Populate the frames with widgets
        self._create_tab1_widgets()
        self._create_tab2_widgets()

    def _create_tab1_widgets(self):
        label = ttk.Label(self.frame1, text="This is Tab 1")
        label.pack(pady=20)

        button = ttk.Button(self.frame1, text="Button in Tab 1")
        button.pack(pady=20)

        def on_button1_click():
            messagebox.showinfo("Info", "Button in Tab 1 clicked!")

        button.config(command=on_button1_click)

    def _create_tab2_widgets(self):
        label2 = ttk.Label(self.frame2, text="This is Tab 2")
        label2.pack(pady=20)

        button2 = ttk.Button(self.frame2, text="Button in Tab 2")
        button2.pack(pady=20)

        def on_button2_click():
            messagebox.showinfo("Info", "Button in Tab 2 clicked!")

        button2.config(command=on_button2_click)


if __name__ == "__main__":
    app = App()
    app.mainloop()
