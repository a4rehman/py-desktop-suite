import math
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pro Calculator")
        self.geometry("380x540")
        self.resizable(False, False)

        self.expression = ""
        self.history = ""

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # Header / History Display
        self.history_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family="Inter", size=14),
            text_color="#8E8E93",
            anchor="e"
        )
        self.history_label.pack(fill="x", padx=20, pady=(20, 5))

        # Main Result / Display Screen
        self.display = ctk.CTkLabel(
            self,
            text="0",
            font=ctk.CTkFont(family="Inter", size=38, weight="bold"),
            text_color="#FFFFFF",
            anchor="e"
        )
        self.display.pack(fill="x", padx=20, pady=(0, 20))

        # Divider
        divider = ctk.CTkFrame(self, height=2, fg_color="#2C2C2E")
        divider.pack(fill="x", padx=20, pady=(0, 15))

        # Buttons Grid Frame
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        for i in range(5):
            grid_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            grid_frame.grid_columnconfigure(j, weight=1)

        buttons = [
            ("C", 0, 0, "#FF453A", "#D1342B", self.on_clear),
            ("⌫", 0, 1, "#3A3A3C", "#48484A", self.on_backspace),
            ("%", 0, 2, "#3A3A3C", "#48484A", lambda: self.on_operator("%")),
            ("/", 0, 3, "#FF9F0A", "#D98200", lambda: self.on_operator("/")),

            ("7", 1, 0, "#2C2C2E", "#3A3A3C", lambda: self.on_digit("7")),
            ("8", 1, 1, "#2C2C2E", "#3A3A3C", lambda: self.on_digit("8")),
            ("9", 1, 2, "#2C2C2E", "#3A3A3C", lambda: self.on_digit("9")),
            ("×", 1, 3, "#FF9F0A", "#D98200", lambda: self.on_operator("*")),

            ("4", 2, 0, "#2C2C2E", "#3A3A3C", lambda: self.on_digit("4")),
            ("5", 2, 1, "#2C2C2E", "#3A3A3C", lambda: self.on_digit("5")),
            ("6", 2, 2, "#2C2C2E", "#3A3A3C", lambda: self.on_digit("6")),
            ("-", 2, 3, "#FF9F0A", "#D98200", lambda: self.on_operator("-")),

            ("1", 3, 0, "#2C2C2E", "#3A3A3C", lambda: self.on_digit("1")),
            ("2", 3, 1, "#2C2C2E", "#3A3A3C", lambda: self.on_digit("2")),
            ("3", 3, 2, "#2C2C2E", "#3A3A3C", lambda: self.on_digit("3")),
            ("+", 3, 3, "#FF9F0A", "#D98200", lambda: self.on_operator("+")),

            ("0", 4, 0, "#2C2C2E", "#3A3A3C", lambda: self.on_digit("0")),
            (".", 4, 1, "#2C2C2E", "#3A3A3C", lambda: self.on_digit(".")),
            ("√", 4, 2, "#3A3A3C", "#48484A", self.on_sqrt),
            ("=", 4, 3, "#30D158", "#24A143", self.on_equals),
        ]

        for text, row, col, bg_color, hover_color, cmd in buttons:
            btn = ctk.CTkButton(
                grid_frame,
                text=text,
                font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
                fg_color=bg_color,
                hover_color=hover_color,
                corner_radius=16,
                command=cmd
            )
            btn.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

    def _bind_keys(self):
        self.bind("<Key>", self._handle_keypress)

    def _handle_keypress(self, event):
        char = event.char
        if char.isdigit() or char == ".":
            self.on_digit(char)
        elif char in ["+", "-", "*", "/"]:
            self.on_operator(char)
        elif event.keysym == "Return":
            self.on_equals()
        elif event.keysym == "BackSpace":
            self.on_backspace()
        elif event.keysym == "Escape":
            self.on_clear()

    def on_digit(self, digit):
        if self.expression == "0" and digit != ".":
            self.expression = digit
        else:
            self.expression += digit
        self._update_display()

    def on_operator(self, op):
        if not self.expression and op == "-":
            self.expression = "-"
        elif self.expression and self.expression[-1] not in "+-*/%":
            self.expression += op
        self._update_display()

    def on_clear(self):
        self.expression = ""
        self.history = ""
        self.history_label.configure(text="")
        self.display.configure(text="0")

    def on_backspace(self):
        self.expression = self.expression[:-1]
        self._update_display()

    def on_sqrt(self):
        try:
            val = float(self.expression) if self.expression else 0
            if val < 0:
                self.display.configure(text="Error")
                return
            res = math.sqrt(val)
            self.history = f"√({self.expression})"
            self.expression = f"{res:.6g}"
            self.history_label.configure(text=self.history)
            self.display.configure(text=self.expression)
        except Exception:
            self.display.configure(text="Error")

    def on_equals(self):
        if not self.expression:
            return
        try:
            self.history = self.expression
            safe_expr = self.expression.replace("×", "*").replace("÷", "/")
            result = eval(safe_expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expression = str(result)
            self.history_label.configure(text=f"{self.history} =")
            self.display.configure(text=self.expression)
        except Exception:
            self.display.configure(text="Error")

    def _update_display(self):
        text = self.expression if self.expression else "0"
        self.display.configure(text=text)


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
