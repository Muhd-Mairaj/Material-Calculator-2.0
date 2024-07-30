import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox, ttk

import openpyxl
from material_calculator.calculator import Calculator
from material_calculator.sheet import Sheet

from .custom_widgets import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Material Calculator")
        # self.geometry("400x300")
        self._center_app(400, 300)

        self._create_styles()
        self._create_widgets()

    def _center_app(self, required_width, required_height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_right = int(screen_width/2 - required_width/2)
        position_down = int(screen_height/2 - required_height/2)
        self.geometry(
            f"{required_width}x{required_height}+{position_right}+{position_down}")

    def _create_styles(self):
        style = ttk.Style()
        style.configure("TFrame", background='#A5C4D4')

    def _create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Create frames for each tab
        self.frame1 = ttk.Frame(self.notebook, style="TFrame")
        self.frame2 = ttk.Frame(self.notebook, style="TFrame")

        # Add frames to the notebook
        self.notebook.add(self.frame1, text="Excel File")
        self.notebook.add(self.frame2, text="Enter Values")

        # Populate the frames with widgets
        self._create_tab1_widgets()
        self._create_tab2_widgets()

    def _create_tab1_widgets(self):
        label = CustomLabel(self.frame1, text="This is Tab 2")
        label.pack(pady=20)

        button = CustomButton(self.frame1, text="Button in Tab 2")
        button.pack(pady=20)

        def on_button_click():
            filename = fd.askopenfilename(
                title="Select a file",
                filetypes=(("Excel Worksheet", "*.xlsx"),),
            )

            if not filename:
                print("yes")
                raise NotImplementedError("Currently not handling file not selected")

            wb = openpyxl.load_workbook(filename, read_only=True)
            sheet = Sheet(wb.active)

            print(sheet.profiles)

        button.config(command=on_button_click)

    def _create_tab2_widgets(self):
        # create label and entry for item length
        length_label = CustomLabel(self.frame2, text="Enter item length:")
        length_label.grid(padx=30, pady=10, row=1, column=1, sticky="w")

        length_entry = ttk.Entry(self.frame2)
        length_entry.grid(padx=30, pady=10, row=1, column=2)

        # create label and entry for item quantity
        quantity_label = CustomLabel(self.frame2, text="Enter item quantity:")
        quantity_label.grid(padx=30, pady=10, row=2, column=1, sticky="w")

        quantity_entry = ttk.Entry(self.frame2)
        quantity_entry.grid(padx=30, pady=10, row=2, column=2)

        button = CustomButton(self.frame2, text="Done")
        button.grid(padx=30, pady=20, row=3, column=2)

        def on_button_click():
            messagebox.showinfo("Info", "Button in Tab 1 clicked!")

        button.config(command=on_button_click)
