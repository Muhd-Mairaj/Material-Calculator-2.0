import os
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import Listbox
from tkinter import Widget
import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *

import openpyxl
from custom_sheets import get_sheet
from custom_sheets.my_sheets import MyReadOnlyWorksheet, MyWorksheet
from material_calculator import Calculator
from material_calculator.helper import check_which_better

from .custom_widgets import *


class App(tb.Window):
    def __init__(self):
        self._data1: dict[int, int] = {}    # data for tab1
        self._data2: dict[int, int] = {}    # data for tab2
        self._sheet: MyReadOnlyWorksheet | MyWorksheet | None = None     # this is only set if an excel sheet is used
        self._toplevel = None

        super().__init__(title="Material Calculator", themename="darkly", resizable=(False, False))
        self.option_add("*Font", ("cambria", 10))
        self._create_widgets()
        self.place_window_center()

        # self.title("Material Calculator")
        # self._center_app(400, 450)
        # self._create_styles()

    @property
    def data1(self) -> dict[int, int]:
        return self._data1.copy()

    @property
    def data2(self) -> dict[int, int]:
        return self._data2.copy()

    # def _center_app(self, required_width: int, required_height: int):
    #     """Centers the application window

    #     Args:
    #         required_width (int): The required width of the centered application window
    #         required_height (int): The required height of the centered application window
    #     """
    #     screen_width = self.winfo_screenwidth()
    #     screen_height = self.winfo_screenheight()
    #     position_right = int(screen_width/2 - required_width/2)
    #     position_down = int(screen_height/2 - required_height/2)
    #     self.geometry(f"{required_width}x{required_height}+{position_right}+{position_down}")

    # def _create_styles(self):
    #     style = ttk.Style()
    #     style.configure("TFrame", background='#A5C4D4')

    def _create_widgets(self):
        self.notebook = tb.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Create frames for each tab
        self.frame1 = tb.Frame(self.notebook)
        self.frame2 = tb.Frame(self.notebook)

        # Add frames to the notebook
        self.notebook.add(self.frame1, text="Excel File")
        self.notebook.add(self.frame2, text="Enter Values")

        # Populate the frames with widgets
        self._create_tab1_widgets()
        self._create_tab2_widgets()

    def _create_tab1_widgets(self):
        # create methods for buttons
        def on_select_button_click():
            # reset previous tree widget
            self._clear_tree(tree)
            
            filename = fd.askopenfilename(
                title="Select a file",
                filetypes=(("Excel Worksheet", "*.xlsx"),),
            )
            # filename = r"C:\Users\rayya\OneDrive\Desktop\GITHUB\32-Bit Python Programs\working\new\resources\Part_List.xlsx"
            if not filename:
                self._sheet = None
                label.config(text="No file selected", bootstyle="default")
                raise NotImplementedError("Currently not handling file not selected")

            wb = openpyxl.load_workbook(filename, read_only=True)
            self._sheet = get_sheet(wb.active)
            profiles = self._sheet.profiles

            for profile in profiles:
                self._add_values_tree(tree, (profile,))

            basename = os.path.basename(filename)
            label.config(text=basename, bootstyle="success")
            instruction_label.pack_forget()
            # instruction_label.configure(text="Select profile to continue")
            done_button.configure(state="enable")
            reset_button.configure(state="enable")

        def on_done_button_click():
            if not self._sheet:
                return

            iid = tree.focus()
            if not iid:
                messagebox.showwarning("Invalid profile", "Please choose one of the available profiles")
                return

            profile, *_ = tree.item(iid, "values")
            self._data1 = self._sheet.get_items(profile)

            print("Calculating best result on:")
            print(self._data1)

            self._analyse_data(self.data1)

        def on_reset_button_click():
            if not self._sheet:
                reset_button.config(state="disable")
                print("No item to clear")
                return

            value = messagebox.askyesno("Confirm?", "Are you sure you want to reset the table?")
            if value:
                self._clear_tree(tree)
                self._data1.clear()
                label.configure(text="No file selected", bootstyle="default")
                instruction_label.pack(pady=(10,20))
                # instruction_label.configure(text="Select file to continue")
                done_button.configure(state="disable")
                reset_button.configure(state="disable")

        # create widgets
        label = BCustomLabel(self.frame1, text="No file selected")
        label.pack(pady=(30, 0))

        select_button = BCustomButton(self.frame1, text="Select file")
        select_button.pack(pady=20)

        tree = self._create_tree(self.frame1, columns=("Profiles",))
        tree.configure(selectmode="browse")
        tree.pack(padx=20, pady=10, expand=True, fill="both")

        frame = tb.Frame(self.frame1)
        frame.pack(pady=(10,0))

        reset_button = BCustomButton(frame, text="Reset", bootstyle="danger")
        reset_button.pack(padx=10, pady=(10,10), side="left")

        done_button = BCustomButton(frame, text="Done")
        done_button.pack(padx=10, pady=(10,10), side="right")

        instruction_label = BCustomLabel(self.frame1, text="Select file to continue", bootstyle="warning")
        instruction_label.pack(pady=(10,20))

        # configure buttons
        tree.bind("<Return>", lambda event: on_done_button_click())
        select_button.config(command=on_select_button_click)
        reset_button.config(state="disable", command=on_reset_button_click)
        done_button.config(state="disable", command=on_done_button_click)

    def _create_tab2_widgets(self):
        # create methods for buttons
        def on_remove_button_click():
            # get iid of row to remove
            iid_range = tree.selection()
            print(iid_range)
            if not iid_range:
                return

            # get values for rows to remove, and remove rows
            for iid in iid_range:
                length, _ = tree.item(iid, "values")

                tree.delete(iid)
                del self._data2[int(length)]

            length_entry.focus()
            if not tree.get_children():
                reset_button.config(state="disable")

        def on_add_button_click():
            length = length_entry.get().strip()
            quantity = quantity_entry.get().strip()

            if not quantity.isdigit() or not length.isdigit():
                raise TypeError("Invalid length or quantity")

            if int(length) > selected_length.get():
                messagebox.showwarning("Invalid Length Entry", f"Item length must be within {selected_length.get()} mm.")
                return

            if int(length) in self._data2:
                self._update_values_tree(tree, (length, self._data2[int(length)] + int(quantity)))
            else:
                self._add_values_tree(tree, (length, quantity))

            self._data2[int(length)] = self._data2.get(int(length), 0) + int(quantity)

            length_entry.delete(0, "end")
            quantity_entry.delete(0, "end")

            length_entry.focus()
            reset_button.config(state="enable")

        def on_reset_button_click():
            if not self.data2:
                reset_button.config(state="disable")
                print("No item to clear")
                return

            value = messagebox.askyesno("Confirm?", "Are you sure you want to reset the table?")
            if value:
                self._clear_tree(tree)
                self._data2.clear()

        def on_done_button_click():
            # messagebox.showinfo("Info", "Button in Tab 1 clicked!")
            print(self._data2)
            self._analyse_data(self._data2)

        # row 1
        # create label and entry for item length
        length_label = tb.Label(self.frame2, text="Enter item length (mm):", width=30)
        length_label.grid(padx=(20,0), pady=(30,15), row=1, column=1, columnspan=2, sticky="w")

        length_entry = tb.Entry(self.frame2, width=15)
        length_entry.grid(padx=20, pady=(30,15), row=1, column=3)

        # row 2
        # create label and entry for item quantity
        quantity_label = tb.Label(self.frame2, text="Enter item quantity (mm):", width=30)
        quantity_label.grid(padx=(20,0), pady=(0,15), row=2, column=1, columnspan=2, sticky="w")

        quantity_entry = tb.Entry(self.frame2, width=15)
        quantity_entry.grid(padx=20, pady=(0,15), row=2, column=3)

        # row 3
        # Add radiobutton for material length
        selected_length = tb.IntVar(value=12000)
        radio1 = tb.Radiobutton(self.frame2, bootstyle="info", text="12 meter", variable=selected_length, value=12000)
        radio2 = tb.Radiobutton(self.frame2, bootstyle="info", text="6 meter", variable=selected_length, value=6000)
        radio1.grid(padx=(20,0), pady=15, row=3, column=1)
        radio2.grid(padx=(20,0), pady=15, row=3, column=2)

        # add Add button
        add_button = BCustomButton(self.frame2, text="Add")
        add_button.grid(pady=(10,20), row=3, column=3)

        # row 4
        # Add table to view items added
        tree = self._create_tree(self.frame2, columns=("Item", "Quantity"))
        tree.grid(padx=20, pady=15, row=4, column=1, columnspan=3, sticky="news")
        
        # configure row 4 to have a minsize of 400
        self.frame2.rowconfigure(4, minsize=400)

        # row 5
        # Add remove, add and done buttons
        reset_button = BCustomButton(self.frame2, text="Reset", bootstyle="danger")
        reset_button.grid(padx=(20,0), pady=(10,20), row=5, column=1)

        remove_button = BCustomButton(self.frame2, text="Remove", bootstyle="danger outline")
        remove_button.grid(padx=(0,20), pady=(10,20), row=5, column=2, sticky="e")
        # remove_button.grid(padx=(20,0), pady=(10,20), row=5, column=1)

        done_button = BCustomButton(self.frame2, text="Done", bootstyle="")
        done_button.grid(pady=(10,20), row=5, column=3)

        # configure button click commands
        remove_button.config(command=on_remove_button_click)
        add_button.config(command=on_add_button_click)
        done_button.config(command=on_done_button_click)
        reset_button.config(state="disable", command=on_reset_button_click)

        # Set keyboard bindings
        length_entry.focus_set()    # start with focus on length_entry
        length_entry.bind("<Return>", lambda event: quantity_entry.focus())
        quantity_entry.bind("<Return>", lambda event: on_add_button_click())
        tree.bind("<KeyPress-Delete>", lambda event: on_remove_button_click())

    def _create_tree(self, root, columns: tuple[str, ...]) -> tb.Treeview:
        # Create a Treeview widget
        tree = tb.Treeview(root, bootstyle="primary", columns=columns)

        # Format columns
        tree.column("#0", width=0, stretch=0)  # The first column
        for column in columns:
            tree.column(column, anchor="w", width=120)

        # Create headings
        tree.heading("#0", text="", anchor="w")
        for column in columns:
            tree.heading(column, text=column, anchor="w")

         # Add scrollbar
        scrollbar = tb.Scrollbar(tree, bootstyle="round info", orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        return tree

    def _clear_tree(self, tree: tb.Treeview):
        for item in tree.get_children():
            tree.delete(item)

    def _add_values_tree(self, tree: tb.Treeview, data: tuple, append: bool = True):
        if not append:
            self._clear_tree(tree)

        # get last iid
        last_iid = 0;
        children = tree.get_children()
        if children:
            last_iid = int(children[-1])

        # if isinstance(data, dict):
        #     # Insert data into the table
        #     for i, values in enumerate(data.items()):
        #         tree.insert(parent='', index='end', iid=last_iid++1+i, text='', values=values)
        if isinstance(data, tuple):
            tree.insert(parent='', index='end', iid=last_iid+1, text='', values=data)
        else:
            raise TypeError

    def _update_values_tree(self, tree: tb.Treeview, data: tuple):
        for item in tree.get_children():
            if tree.item(item, "values")[0] == data[0]:
                tree.item(item, values=data)
                break

    def _analyse_data(self, data: dict[int, int], material_length: int = -1):
        c1 = Calculator(data, material_length, "Sort")
        required1, scrap1, excess1 = c1.solve()
        c1.print_stats(required1, scrap1, excess1)

        c2 = Calculator(data, material_length, "Adapted Sort")
        required2, scrap2, excess2 = c2.solve()
        c2.print_stats(required2, scrap2, excess2)

        print(check_which_better((c1, c2)))
        best = min([c1, c2])
        print(best.method)
        print(best.work_order)

        self._create_display_window(best)

    def _create_display_window(self, best: Calculator):
        def on_closing():
            # self.deiconify()
            self._toplevel.destroy()

        # self.withdraw()
        if self._toplevel:
            self._toplevel.destroy()

        required, scrap, excess = best.results

        self._toplevel = tb.Toplevel(
            title="Best Results",
            resizable=(False, False),
            topmost=True,
        )

        # bind window close event to show the root window
        self._toplevel.protocol("WM_DELETE_WINDOW", on_closing)

        # row 1 - required
        required_label = BCustomLabel(self._toplevel, text="Required:", width=27)
        required_label.grid(padx=20, pady=20, row=1, column=1, sticky="w")

        required_text = tb.Text(self._toplevel, wrap='word', height=-1, width=15)
        required_text.insert("1.0", required)
        required_text.config(state="disabled")
        required_text.grid(padx=20, pady=20, row=1, column=2, sticky="e")

        # row 2 - scrap
        scrap_label = BCustomLabel(self._toplevel, text="Scrap:", width=27)
        scrap_label.grid(padx=20, pady=(0,20), row=2, column=1, sticky="w")

        scrap_text = tb.Text(self._toplevel, wrap='word', height=-1, width=15)
        scrap_text.insert("1.0", scrap)
        scrap_text.config(state="disabled")
        scrap_text.grid(padx=20, pady=(0,20), row=2, column=2, sticky="e")

        # row 3 - excess
        excess_label = BCustomLabel(self._toplevel, text="Excess:", width=27)
        excess_label.grid(padx=20, pady=(0,20), row=3, column=1, sticky="w")

        excess_text = tb.Text(self._toplevel, wrap='word', height=-1, width=15)
        excess_text.insert("1.0", excess)
        excess_text.config(state="disabled")
        excess_text.grid(padx=20, pady=(0,20), row=3, column=2, sticky="e")

        # row 4 - work order
        work_order_label = BCustomLabel(self._toplevel, text="Work Order:", width=15)
        work_order_label.grid(padx=20, pady=(0,10), row=4, column=1, sticky="w")

        # scrolled_frame = ScrolledFrame(self._toplevel)
        # scrolled_frame.grid(row=5, column=1, columnspan=2, sticky="news")

        listbox = Listbox(self._toplevel, borderwidth=12)
        # listbox.pack(pady=10, expand=1, fill="both")
        listbox.grid(padx=20, pady=(0,20), row=5, column=1, columnspan=2, sticky="news")
        self._toplevel.rowconfigure(5, minsize=400)

        vscrollbar = tb.Scrollbar(listbox, bootstyle="round info", orient="vertical", command=listbox.yview)
        listbox.configure(yscroll=vscrollbar.set)
        vscrollbar.pack(side="right", fill="y")

        hscrollbar = tb.Scrollbar(listbox, bootstyle="round info", orient="horizontal", command=listbox.xview)
        listbox.configure(xscrollcommand=hscrollbar.set)
        hscrollbar.pack(side="bottom", fill="x")

        return_button = BCustomButton(self._toplevel, text="Return")
        return_button.grid(pady=(0,20), row=6, column=1, columnspan=2)

        for i, row in enumerate(best.work_order, 1):
            listbox.insert(i, ", ".join([str(item) for item in row]))

        return_button.config(command=on_closing)

        # self._toplevel.place_window_center()
        self._toplevel.focus_force()
        self._toplevel.mainloop()

    def _clear_window(self, widget: Widget):
        for child in widget.winfo_children():
            child.destroy()

    # def _remove_values(self, tree: tb.Treeview, data: dict[int, int]):
    #     # get iid of row to remove
    #     iid_range = tree.selection()
    #     print(iid_range)
    #     if not iid_range:
    #         return

    #     # get values for rows to remove, and remove rows
    #     for iid in iid_range:
    #         length, _ = tree.item(iid, "values")

    #         tree.delete(iid)
    #         del data[int(length)]

