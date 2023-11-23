import tkinter as tk
import threading

# Функция для создания и отображения второго окна
def create_second_window():
    second_window = tk.Toplevel(root)
    second_window.title("Второе окно")
    label = tk.Label(second_window, text="Это второе окно")
    label.pack()

# Функция, которая будет вызывать create_second_window в другом потоке
def open_second_window():
    second_window_thread = threading.Thread(target=create_second_window)
    second_window_thread.start()

# Основное окно
root = tk.Tk()
root.title("Основное окно")

# Кнопка для открытия второго окна
open_button = tk.Button(root, text="Открыть второе окно", command=open_second_window)
open_button.pack()

root.mainloop()
