import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
import os

# --- Конфигурация приложения ---
HISTORY_FILE = "history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32

# Цветовая палитра
BG_MAIN = "#2c3e50"
BG_SECONDARY = "#34495e"
ACCENT = "#3498db"
TEXT_COLOR = "#ecf0f1"


def generate_password(length, use_digits, use_letters, use_special):
    """Генерация случайной последовательности символов."""
    if length < 1:
        raise ValueError("Длина должна быть больше нуля.")

    pool = ''
    if use_digits: pool += string.digits
    if use_letters: pool += string.ascii_letters
    if use_special: pool += string.punctuation

    if not pool:
        raise ValueError("Необходимо выбрать хотя бы один тип символов.")

    return ''.join(random.choices(pool, k=length))


def load_history():
    """Загрузка истории из локального JSON файла."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_history(history):
    """Сохранение последних записей в файл."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history[-15:], f, ensure_ascii=False, indent=2)


def update_table():
    """Обновление данных в виджете таблицы."""
    for item in tree.get_children():
        tree.delete(item)
    for pwd in reversed(load_history()):
        tree.insert('', 'end', values=(pwd,))


def on_generate():
    """Обработка нажатия кнопки генерации."""
    try:
        length = int(scale_len.get())

        if not (MIN_LENGTH <= length <= MAX_LENGTH):
            messagebox.showwarning("Внимание", f"Длина должна быть от {MIN_LENGTH} до {MAX_LENGTH}")
            return

        new_pwd = generate_password(length, var_dig.get(), var_let.get(), var_spec.get())

        # Здесь переменная entry_res должна быть уже создана в основной части кода ниже
        entry_res.delete(0, tk.END)
        entry_res.insert(0, new_pwd)

        current_history = load_history()
        current_history.append(new_pwd)
        save_history(current_history)
        update_table()

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))


# --- Инициализация GUI ---
root = tk.Tk()
root.title("Password Generator")
root.geometry("500x520")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

# Стилизация элементов ttk
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", background=BG_SECONDARY, foreground=TEXT_COLOR,
                fieldbackground=BG_SECONDARY, rowheight=25, borderwidth=0)
style.configure("Treeview.Heading", background="#1abc9c", foreground="white", font=('Segoe UI', 10, 'bold'))
style.map("Treeview.Heading", background=[('active', '#16a085')])

# Панель настроек
top_frame = tk.Frame(root, bg=BG_MAIN, pady=20)
top_frame.pack()

tk.Label(top_frame, text="Длина:", bg=BG_MAIN, fg=TEXT_COLOR, font=("Arial", 10, "bold")).grid(row=0, column=0)
scale_len = tk.Scale(top_frame, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL,
                     length=220, bg=BG_MAIN, fg=ACCENT, highlightthickness=0, troughcolor=BG_SECONDARY)
scale_len.set(12)
scale_len.grid(row=0, column=1, columnspan=2, padx=10)

var_dig, var_let, var_spec = tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True)

cb_style = {"bg": BG_MAIN, "fg": TEXT_COLOR, "activebackground": BG_MAIN, "selectcolor": BG_SECONDARY}
tk.Checkbutton(top_frame, text="Цифры", variable=var_dig, **cb_style).grid(row=1, column=0, pady=15)
tk.Checkbutton(top_frame, text="Буквы", variable=var_let, **cb_style).grid(row=1, column=1)
tk.Checkbutton(top_frame, text="Символы", variable=var_spec, **cb_style).grid(row=1, column=2)

# Кнопка действия
btn_run = tk.Button(root, text="СГЕНЕРИРОВАТЬ", command=on_generate, bg=ACCENT, fg="white",
                    font=("Arial", 11, "bold"), relief="flat", padx=20, pady=5)
btn_run.pack(pady=10)

# Поле вывода результата (entry_res)
entry_res = tk.Entry(root, font=("Consolas", 15), width=25, justify="center",
                     bg=TEXT_COLOR, relief="flat")
entry_res.pack(pady=10)

# Секция истории (таблица)
hist_frame = tk.Frame(root, bg=BG_MAIN)
hist_frame.pack(fill="both", expand=True, padx=30, pady=20)

tree = ttk.Treeview(hist_frame, columns=('pwd',), show='headings')
tree.heading('pwd', text='ИСТОРИЯ ПАРОЛЕЙ')
tree.column('pwd', anchor="center", width=400)
tree.pack(side="left", fill="both", expand=True)

scroll = ttk.Scrollbar(hist_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
scroll.pack(side="right", fill="y")

# Загрузка данных при старте
update_table()

root.mainloop()