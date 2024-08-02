import ttkbootstrap as tb


class BCustomLabel(tb.Label):
    def __init__(self, master, *args, **kwargs):
        kwargs.setdefault("font", ("", 10))
        super().__init__(master, *args, **kwargs)


class BCustomButton(tb.Button):
    def __init__(self, master, *args, **kwargs):
        kwargs.setdefault("width", 10)
        super().__init__(master, *args, **kwargs)


# class CustomLabel(ttk.Label):
#     custom_style = "Custom.TLabel"

#     def __init__(self, master, *args, **kwargs):
#         self.create_custom_style(CustomLabel.custom_style)

#         kwargs.setdefault("style", CustomLabel.custom_style)
#         super().__init__(master, *args, **kwargs)

#     def create_custom_style(self, style_name):
#         style = ttk.Style()
#         style.configure(style_name, background='#A5C4D4', foreground='#2D232E')


# class CustomButton(ttk.Button):
#     custom_style = "Custom.TButton"

#     def __init__(self, master, *args, **kwargs):
#         self.create_custom_style(CustomButton.custom_style)

#         kwargs.setdefault("style", CustomButton.custom_style)
#         super().__init__(master, *args, **kwargs)

#     def create_custom_style(self, style_name):
#         style = ttk.Style()
#         style.configure(style_name, background='#D56F3E', foreground='#2D232E')
