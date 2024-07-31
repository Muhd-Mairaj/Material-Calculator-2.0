import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox, ttk

import openpyxl
from material_calculator import Calculator
from custom_sheets import get_sheet

from .custom_widgets import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.data = {}
        self.title("Material Calculator")
        self._center_app(400, 450)

        self._create_styles()
        self._create_widgets()

    def _center_app(self, required_width: int, required_height: int):
        """Centers the application window

        Args:
            required_width (int): The required width of the centered application window
            required_height (int): The required height of the centered application window
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_right = int(screen_width/2 - required_width/2)
        position_down = int(screen_height/2 - required_height/2)
        self.geometry(f"{required_width}x{required_height}+{position_right}+{position_down}")

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
        label = CustomLabel(self.frame1, text="No file selected")
        label.pack(pady=(20, 0))

        select_button = CustomButton(self.frame1, text="Select file")
        select_button.pack(pady=20)

        tree = self.create_table(self.frame1)
        tree.pack(padx=20, pady=10, expand=True, fill="both")
        tree.bind("<KeyPress-Delete>", lambda event: self._remove_values(tree, self.data))
        # tree.bind("<KeyPress-Delete>", lambda event: length_entry.focus(), add="+")

        done_button = CustomButton(self.frame1, text="Done")
        done_button.pack(pady=10)
        done_button.configure(state="disable")

        def on_select_button_click():
            filename = fd.askopenfilename(
                title="Select a file",
                filetypes=(("Excel Worksheet", "*.xlsx"),),
            )

            if not filename:
                raise NotImplementedError("Currently not handling file not selected")

            basename = os.path.basename(filename)
            label.config(text=basename, foreground="#2b4d2a")
            self.update_idletasks()

            wb = openpyxl.load_workbook(filename, read_only=True)
            sheet = get_sheet(wb.active)

            print(sheet.profiles)
            print(sheet.profiles[0])
            print(sheet.get_items(sheet.profiles[0]))

            self.data = sheet.get_items(sheet.profiles[0])
            self._add_values(tree, self.data)

            done_button.configure(state="enable")

        def on_done_button_click():
            print(self.data)

        select_button.config(command=on_select_button_click)
        done_button.config(command=on_done_button_click)

    def _create_tab2_widgets(self):
        # create label and entry for item length
        length_label = CustomLabel(self.frame2, text="Enter item length (mm):", width=35)
        length_label.grid(padx=(20,0), pady=(20,10), row=1, column=1, columnspan=2, sticky="w")

        length_entry = ttk.Entry(self.frame2)
        length_entry.focus_set()
        length_entry.bind("<Return>", lambda event: quantity_entry.focus())
        length_entry.grid(padx=20, pady=(20,10), row=1, column=3)

        # create label and entry for item quantity
        quantity_label = CustomLabel(self.frame2, text="Enter item quantity (mm):", width=35)
        quantity_label.grid(padx=(20,0), pady=(0,10), row=2, column=1, columnspan=2, sticky="w")

        quantity_entry = ttk.Entry(self.frame2)
        # quantity_entry.bind("<Return>", lambda event: add_values())
        quantity_entry.bind("<Return>", lambda event: length_entry.focus(), add="+") # add="+" specifies that other bound functions should not be replaced
        quantity_entry.grid(padx=20, pady=(0,10), row=2, column=3)

        # Add radiobutton for material length

        # Add table to view items added
        tree = self.create_table(self.frame2)
        self.frame2.rowconfigure(4, minsize=250)
        tree.grid(padx=20, pady=(0,10), row=4, column=1, columnspan=3, sticky="news")

        remove_button = CustomButton(self.frame2, text="Remove", command=lambda: self._remove_values(tree, self.data))
        remove_button.grid(padx=(20,0), pady=(0,10), row=5, column=1)

        add_button = CustomButton(self.frame2, text="Add")
        add_button.grid(pady=(0,10), row=5, column=2, sticky="e")

        button = CustomButton(self.frame2, text="Done")
        button.grid(pady=(0,10), row=5, column=3)

        def on_button_click():
            messagebox.showinfo("Info", "Button in Tab 1 clicked!")

        button.config(command=on_button_click)

    def create_table(self, root) -> ttk.Treeview:
        # Create a Treeview widget
        tree = ttk.Treeview(root)

        # Define columns
        tree["columns"] = ("Item", "Quantity")

        # Format columns
        tree.column("#0", width=0, stretch=0)  # The first column
        tree.column("Item", anchor="w", width=120)
        tree.column("Quantity", anchor="w", width=120)

        # Create headings
        tree.heading("#0", text="", anchor="w")
        tree.heading("Item", text="Item", anchor="w")
        tree.heading("Quantity", text="Quantity", anchor="w")

         # Add scrollbar
        scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        if self.data:
            self._add_values(tree, self.data)

        return tree

    def _add_values(self, tree: ttk.Treeview, data: dict[int, int] | tuple, append: bool = False):
        if not append:
            # clear treeview
            for child in tree.get_children():
                tree.delete(child)

        # get last iid
        last_iid = 0;
        children = tree.get_children()
        if children:
            last_iid = int(children[-1])

        if isinstance(data, dict):
            # Insert data into the table
            for i, values in enumerate(data.items()):
                tree.insert(parent='', index='end', iid=last_iid++1+i, text='', values=values)
        elif isinstance(data, tuple):
            tree.insert(parent='', index='end', iid=last_iid+1, text='', values=data)

    def _remove_values(self, tree: ttk.Treeview, data: dict[int, int]):
        # get iid of row to remove
        iid_range = tree.selection()
        print(iid_range)
        if not iid_range:
            return

        # get values for rows to remove, and remove rows
        for iid in iid_range:
            length, _ = tree.item(iid, "values")

            tree.delete(iid)
            del data[int(length)]

