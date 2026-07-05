"""
COS202 Assignment - Mathematical Calculator (MC)
-------------------------------------------------
An interactive, screen-based (GUI) simple calculator built with Tkinter.

Supported operations: + - * / (division) \\ (integer/floor division)
                       ^ (power) % (modulus) C (Clear) OFF (Exit)

Author: Kayode
Course: COS202
"""

import tkinter as tk
from tkinter import font as tkfont


class MathematicalCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Mathematical Calculator (MC)")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2f")

        # Internal state
        self.expression = ""
        self.new_number = True   # True if the next digit should start a fresh number
        self.error_state = False

        self._build_display()
        self._build_buttons()

    # ---------------------------------------------------------------
    # UI CONSTRUCTION
    # ---------------------------------------------------------------
    def _build_display(self):
        display_font = tkfont.Font(family="Consolas", size=28, weight="bold")
        self.display_var = tk.StringVar(value="0")

        display_frame = tk.Frame(self.root, bg="#1e1e2f")
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=(15, 5))

        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=display_font,
            bg="#282a3a",
            fg="#00ffcc",
            anchor="e",
            width=14,
            height=2,
            relief="flat",
        )
        self.display.pack(fill="both", expand=True)

    def _build_buttons(self):
        btn_font = tkfont.Font(family="Consolas", size=16, weight="bold")

        # (label, row, col, colspan, bg, fg)
        layout = [
            ("C",   1, 0, 1, "#ff5555", "white"),
            ("OFF", 1, 1, 1, "#990000", "white"),
            ("%",   1, 2, 1, "#3a3d5c", "#00ffcc"),
            ("^",   1, 3, 1, "#3a3d5c", "#00ffcc"),

            ("7",   2, 0, 1, "#33354d", "white"),
            ("8",   2, 1, 1, "#33354d", "white"),
            ("9",   2, 2, 1, "#33354d", "white"),
            ("/",   2, 3, 1, "#3a3d5c", "#00ffcc"),

            ("4",   3, 0, 1, "#33354d", "white"),
            ("5",   3, 1, 1, "#33354d", "white"),
            ("6",   3, 2, 1, "#33354d", "white"),
            ("\\",  3, 3, 1, "#3a3d5c", "#00ffcc"),  # integer/floor division

            ("1",   4, 0, 1, "#33354d", "white"),
            ("2",   4, 1, 1, "#33354d", "white"),
            ("3",   4, 2, 1, "#33354d", "white"),
            ("*",   4, 3, 1, "#3a3d5c", "#00ffcc"),

            ("0",   5, 0, 2, "#33354d", "white"),
            (".",   5, 2, 1, "#33354d", "white"),
            ("-",   5, 3, 1, "#3a3d5c", "#00ffcc"),

            ("=",   6, 0, 3, "#00b894", "white"),
            ("+",   6, 3, 1, "#3a3d5c", "#00ffcc"),
        ]

        for (label, row, col, colspan, bg, fg) in layout:
            btn = tk.Button(
                self.root,
                text=label,
                font=btn_font,
                bg=bg,
                fg=fg,
                relief="flat",
                activebackground="#555577",
                width=5 if colspan == 1 else 12,
                height=2,
                command=lambda l=label: self.on_button_press(l),
            )
            btn.grid(row=row, column=col, columnspan=colspan, padx=4, pady=4, sticky="nsew")

    # ---------------------------------------------------------------
    # LOGIC
    # ---------------------------------------------------------------
    def on_button_press(self, label):
        if label == "OFF":
            self.root.quit()
            return

        if label == "C":
            self.clear()
            return

        if label == "=":
            self.calculate()
            return

        # If we're recovering from an error/result, start fresh unless it's an operator
        if self.error_state:
            self.clear()

        if label in "0123456789.":
            self.display_var.set(
                label if self.new_number else self.display_var.get() + label
            )
            self.new_number = False
        else:
            # Operator pressed (+ - * / \ ^ %)
            current = self.display_var.get()
            self.expression = current + self._translate_operator(label)
            self.new_number = True
            self.display_var.set(current)  # keep showing current number

    @staticmethod
    def _translate_operator(op):
        mapping = {
            "\\": "//",  # integer division
            "^": "**",   # power
        }
        return mapping.get(op, op)

    def calculate(self):
        current = self.display_var.get()
        full_expr = self.expression + current

        try:
            # Only allow safe characters to avoid arbitrary code execution
            allowed = set("0123456789.+-*/%() ")
            safe_expr = full_expr.replace("//", "").replace("**", "")
            if not set(safe_expr).issubset(allowed) and "//" not in full_expr and "**" not in full_expr:
                raise ValueError("Invalid characters")

            result = eval(full_expr, {"__builtins__": {}}, {})
            self.display_var.set(self._format_result(result))
            self.expression = ""
            self.new_number = True
            self.error_state = False
        except ZeroDivisionError:
            self.display_var.set("Error: Div by 0")
            self.error_state = True
        except Exception:
            self.display_var.set("Error")
            self.error_state = True

    @staticmethod
    def _format_result(result):
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    def clear(self):
        self.expression = ""
        self.display_var.set("0")
        self.new_number = True
        self.error_state = False


def main():
    root = tk.Tk()
    app = MathematicalCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
