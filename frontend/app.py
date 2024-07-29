import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from custom_widgets import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Material Calculator")
        self.geometry("400x300")

        self._create_styles()
        self._create_widgets()

    def _create_styles(self):
        # Create a style object
        style = ttk.Style()

        # Define a style for Frames
        style.configure("TFrame", background='#A5C4D4')


    def _create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Create frames for each tab
        self.frame1 = ttk.Frame(self.notebook, style="TFrame")
        self.frame2 = ttk.Frame(self.notebook, style="TFrame")

        # Add frames to the notebook
        self.notebook.add(self.frame1, text="Enter Values")
        self.notebook.add(self.frame2, text="Excel File")

        # Populate the frames with widgets
        self._create_tab1_widgets()
        self._create_tab2_widgets()

    def _create_tab1_widgets(self):
        label = CustomLabel(self.frame1, text="This is Tab 1")
        label.pack(pady=20)

        button = CustomButton(self.frame1, text="Button in Tab 1")
        button.pack(pady=20)

        def on_button_click():
            messagebox.showinfo("Info", "Button in Tab 1 clicked!")

        button.config(command=on_button_click)

    def _create_tab2_widgets(self):
        label = CustomLabel(self.frame2, text="This is Tab 2")
        label.pack(pady=20)

        button = CustomButton(self.frame2, text="Button in Tab 2")
        button.pack(pady=20)

        def on_button_click():
            messagebox.showinfo("Info", "Button in Tab 2 clicked!")

        button.config(command=on_button_click)


if __name__ == "__main__":
    app = App()
    app.mainloop()
