import tkinter as tk
from tkinter import messagebox
import math
import time
from PIL import ImageTk, Image

class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("хуевый шиморенковский калькулятор")
        root.geometry("400x550")
        root.configure(bg="#0000ff")
        root.attributes("-alpha", 0.95)

        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="0")

        try:
            image = Image.open("src/astolfo.png")
            resized_image = image.resize((100, 100), Image.LANCZOS)  
            img = ImageTk.PhotoImage(resized_image)
            self.image_label = tk.Label(root, image=img, bg="#004dff")
            self.image_label.image = img  
            self.image_label.pack(anchor="nw")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл src/astolfo.png не найден!")
            tk.Label(root, text="Изображение не найдено", bg="#004dff", fg="white").pack(anchor="nw")

        self.create_ui()

    def create_ui(self):
        display_frame = tk.Frame(self.root, bg="#0000ff", highlightbackground="blue", highlightthickness=1)
        display_frame.pack(pady=10, fill="both", expand=True)

        tk.Label(display_frame, textvariable=self.expression_var, anchor="e", font=("Arial", 24), bg="#0000ff", fg="#ff0000", padx=10, pady=10).pack(fill="both", expand=True)
        tk.Label(display_frame, textvariable=self.result_var, anchor="e", font=("Arial", 16), bg="#0000ff", fg="#ff0000", padx=10, pady=5).pack(fill="both", expand=True)

        button_frame = tk.Frame(self.root, bg="#0000ff")
        button_frame.pack(fill="both", expand=True)

        buttons = [
            ("7", "#000201"), ("8", "#000201"), ("9", "#000201"), ("/", "#ff00ff"),
            ("4", "#000201"), ("5", "#000201"), ("6", "#000201"), ("*", "#ff00ff"),
            ("1", "#000201"), ("2", "#000201"), ("3", "#000201"), ("-", "#ff00ff"),
            ("0", "#000201"), (".", "#000201"), ("=", "#000201"), ("+", "#ff00ff"),
            ("√", "#35ff19"), ("сын", "#35ff19"), ("cosoi", "#fffd33"), ("аниме тян", "#ffb6c1"),
            ("ln", "#35ff19"), ("exp", "#35ff19"), ("!", "#35ff19"), ("ассемблер", "#fffd33")
        ]

        for i, (text, color) in enumerate(buttons):
            tk.Button(button_frame, text=text, font=("Arial", 18), bg=color, fg="#84fefc", relief="flat",
                      command=lambda t=text: self.on_button_click(t)).grid(row=i // 4 + 1, column=i % 4, padx=5, pady=5, sticky="nsew")

        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)

        root.bind("<Key>", self.on_key_press)

    def on_button_click(self, text):
        actions = {
            "ассемблер": lambda: (self.expression_var.set(""), self.result_var.set("0")),
            "=": self.calculate_result_and_animate,
            "√": lambda: self.function_click("sqrt"),
            "сын": lambda: self.function_click("sin"),
            "cosoi": lambda: self.function_click("cos"),
            "аниме тян": lambda: self.function_click("tan"),
            "ln": lambda: self.function_click("log"),
            "exp": lambda: self.function_click("exp"),
            "!": lambda: self.function_click("factorial")
        }

        if text in actions:
            actions[text]()
        else:
            current_value = self.expression_var.get()
            self.expression_var.set(current_value + text)
            self.calculate_result()

    def function_click(self, func_name):
        self.expression_var.set(f"{func_name}({self.expression_var.get()})")
        self.calculate_result()

    def calculate_result_and_animate(self):
        self.calculate_result()
        self.animate_replace_expression()

    def calculate_result(self):
        try:
            expression = self.expression_var.get()
            expression = expression.replace("sqrt", "math.sqrt")
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("log", "math.log")
            expression = expression.replace("exp", "math.exp")
            expression = expression.replace("factorial", "math.factorial")
            result = eval(expression)
            self.result_var.set(str(result))
        except Exception as e:
            self.result_var.set("Error")

    def animate_replace_expression(self):
        result = self.result_var.get()
        for i in range(1, len(result) + 1):
            self.expression_var.set(result[:i])
            self.root.update()
            time.sleep(0.05)

    def on_key_press(self, event):
        key = event.keysym
        actions = {
            "Return": self.calculate_result_and_animate,
            "BackSpace": lambda: self.expression_var.set(self.expression_var.get()[:-1] if self.expression_var.get() else ""),
            "Escape": lambda: (self.expression_var.set(""), self.result_var.set("0"))
        }
        if key in actions:
            actions[key]()
            if key == "BackSpace":  
                self.calculate_result()
        elif key in "0123456789.+-*/()":
            self.on_button_click(key)
        elif key in ["s", "i", "n", "c", "o", "t", "a", "l", "g", "q", "r", "e", "x", "p", "f", "!"]:
            self.expression_var.set(self.expression_var.get() + key)
            self.calculate_result()

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
