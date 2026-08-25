import tkinter as tk
from tkinter import messagebox
import math
import re

class ScientificCalculator:
    """
    A fully functional, elegant, and robust Scientific Calculator built with tkinter.
    Supports basic arithmetic, advanced scientific functions, memory operations, 
    parentheses, keyboard bindings, and safe expression evaluation.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("SATHISH PANDIAN D | B11-Class 2- Assignment | Scientific Calculator")
        self.root.geometry("420x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        # Memory storage
        self.memory: float = 0.0

        # Current expression variable linked to the display entry
        self.expression_var = tk.StringVar()

        # Build UI components
        self._create_display()
        self._create_buttons()
        self._bind_keyboard()

    def _create_display(self) -> None:
        """Creates the display screen for input and results."""
        display_frame = tk.Frame(self.root, bg="#1e1e1e", padx=10, pady=10)
        display_frame.pack(fill=tk.X)

        self.display_entry = tk.Entry(
            display_frame,
            textvariable=self.expression_var,
            font=("Segoe UI", 22),
            bg="#2d2d2d",
            fg="#ffffff",
            bd=0,
            relief=tk.FLAT,
            justify=tk.RIGHT,
            insertbackground="white"
        )
        self.display_entry.pack(fill=tk.X, ipady=12)

    def _create_buttons(self) -> None:
        """Creates and places the grid of buttons with distinct visual groupings."""
        btn_frame = tk.Frame(self.root, bg="#1e1e1e", padx=10, pady=5)
        btn_frame.pack(fill=tk.BOTH, expand=True)

        # Button layout definition: (Text, Row, Column, BG Color, FG Color)
        buttons = [
            # Row 0: Clear & Memory Controls
            ("CE", 0, 0, "#333333", "#ff5555"),
            ("C", 0, 1, "#333333", "#ff5555"),
            ("⌫", 0, 2, "#333333", "#ffb86c"),
            ("(", 0, 3, "#333333", "#8be9fd"),
            (")", 0, 4, "#333333", "#8be9fd"),

            # Row 1: Scientific Functions 1
            ("sin", 1, 0, "#2b2b2b", "#50fa7b"),
            ("cos", 1, 1, "#2b2b2b", "#50fa7b"),
            ("tan", 1, 2, "#2b2b2b", "#50fa7b"),
            ("π", 1, 3, "#2b2b2b", "#bd93f9"),
            ("e", 1, 4, "#2b2b2b", "#bd93f9"),

            # Row 2: Scientific Functions 2
            ("log", 2, 0, "#2b2b2b", "#50fa7b"),
            ("ln", 2, 1, "#2b2b2b", "#50fa7b"),
            ("sqrt", 2, 2, "#2b2b2b", "#50fa7b"),
            ("^", 2, 3, "#2b2b2b", "#bd93f9"),
            ("!", 2, 4, "#2b2b2b", "#bd93f9"),

            # Row 3: Numbers & Basic Ops 1
            ("7", 3, 0, "#3c3c3c", "#ffffff"),
            ("8", 3, 1, "#3c3c3c", "#ffffff"),
            ("9", 3, 2, "#3c3c3c", "#ffffff"),
            ("/", 3, 3, "#444444", "#ff79c6"),
            ("MC", 3, 4, "#2b2b2b", "#f1fa8c"),

            # Row 4: Numbers & Basic Ops 2
            ("4", 4, 0, "#3c3c3c", "#ffffff"),
            ("5", 4, 1, "#3c3c3c", "#ffffff"),
            ("6", 4, 2, "#3c3c3c", "#ffffff"),
            ("*", 4, 3, "#444444", "#ff79c6"),
            ("MR", 4, 4, "#2b2b2b", "#f1fa8c"),

            # Row 5: Numbers & Basic Ops 3
            ("1", 5, 0, "#3c3c3c", "#ffffff"),
            ("2", 5, 1, "#3c3c3c", "#ffffff"),
            ("3", 5, 2, "#3c3c3c", "#ffffff"),
            ("-", 5, 3, "#444444", "#ff79c6"),
            ("M+", 5, 4, "#2b2b2b", "#f1fa8c"),

            # Row 6: Bottom Row
            ("0", 6, 0, "#3c3c3c", "#ffffff"),
            (".", 6, 1, "#3c3c3c", "#ffffff"),
            ("=", 6, 2, "#ff79c6", "#1e1e1e"),
            ("+", 6, 3, "#444444", "#ff79c6"),
            ("M-", 6, 4, "#2b2b2b", "#f1fa8c"),
        ]

        # Configure grid weights for responsive scaling
        for i in range(7):
            btn_frame.rowconfigure(i, weight=1)
        for j in range(5):
            btn_frame.columnconfigure(j, weight=1)

        # Create buttons and bind actions
        for (text, row, col, bg_color, fg_color) in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Segoe UI", 12, "bold"),
                bg=bg_color,
                fg=fg_color,
                activebackground="#555555",
                activeforeground="#ffffff",
                bd=0,
                relief=tk.FLAT,
                command=lambda t=text: self._on_button_click(t)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

    def _bind_keyboard(self) -> None:
        """Binds keyboard events to allow typing and calculating."""
        self.root.bind("<Return>", lambda event: self._evaluate_expression())
        self.root.bind("<BackSpace>", lambda event: self._on_button_click("⌫"))
        self.root.bind("<Escape>", lambda event: self._on_button_click("C"))

    def _on_button_click(self, char: str) -> None:
        """Handles click events for all calculator buttons."""
        current_text = self.expression_var.get()

        if char == "C":
            self.expression_var.set("")
        elif char == "CE":
            # Clear current entry/number or full clear
            self.expression_var.set("")
        elif char == "⌫":
            self.expression_var.set(current_text[:-1])
        elif char == "=":
            self._evaluate_expression()
        elif char == "MC":
            self.memory = 0.0
            messagebox.showinfo("Memory", "Memory Cleared (MC)")
        elif char == "MR":
            self.expression_var.set(current_text + str(self.memory))
        elif char == "M+":
            try:
                val = eval(self._sanitize_expression(current_text), {"__builtins__": None}, self._get_safe_namespace())
                self.memory += val
            except Exception:
                messagebox.showerror("Error", "Invalid expression for M+")
        elif char == "M-":
            try:
                val = eval(self._sanitize_expression(current_text), {"__builtins__": None}, self._get_safe_namespace())
                self.memory -= val
            except Exception:
                messagebox.showerror("Error", "Invalid expression for M-")
        else:
            # Append symbols, numbers, or functions nicely formatted
            if char in ["sin", "cos", "tan", "log", "ln", "sqrt"]:
                self.expression_var.set(current_text + f"{char}(")
            elif char == "^":
                self.expression_var.set(current_text + "^")
            elif char == "!":
                self.expression_var.set(current_text + "!")
            elif char == "π":
                self.expression_var.set(current_text + "π")
            elif char == "e":
                self.expression_var.set(current_text + "e")
            else:
                self.expression_var.set(current_text + char)

    def _sanitize_expression(self, expr: str) -> str:
        """Transforms user-friendly mathematical notation into valid Python syntax."""
        # Replace constants
        expr = expr.replace("π", "pi")
        
        # Replace power operator ^ with **
        expr = expr.replace("^", "**")

        # Handle factorials (e.g., '5!' -> 'factorial(5)')
        expr = re.sub(r'(\d+)!', r'factorial(\1)', expr)

        return expr

    def _get_safe_namespace(self) -> dict:
        """Returns a safe dictionary of allowed mathematical functions and constants."""
        return {
            "sin": lambda x: math.sin(math.radians(x)),  # Degree mode default for user convenience
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log10,
            "ln": math.log,
            "sqrt": math.sqrt,
            "factorial": math.factorial,
            "pi": math.pi,
            "e": math.e,
            "abs": abs
        }

    def _evaluate_expression(self) -> None:
        """Safely evaluates the mathematical expression on the display."""
        raw_expr = self.expression_var.get()
        if not raw_expr.strip():
            return

        try:
            sanitized_expr = self._sanitize_expression(raw_expr)
            result = eval(sanitized_expr, {"__builtins__": None}, self._get_safe_namespace())
            
            # Format floating point results nicely (remove trailing .0 if integer)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            self.expression_var.set(str(result))
        except ZeroDivisionError:
            self.expression_var.set("Error")
            messagebox.showerror("Math Error", "Division by zero is undefined.")
        except (ValueError, TypeError, OverflowError):
            self.expression_var.set("Error")
            messagebox.showerror("Domain Error", "Invalid mathematical operation (e.g., log/sqrt of negative number).")
        except Exception:
            self.expression_var.set("Error")
            messagebox.showerror("Syntax Error", "Invalid expression syntax.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()