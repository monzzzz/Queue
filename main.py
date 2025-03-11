import tkinter as tk
from collections import deque
from datetime import datetime

import tkinter as tk
from collections import deque
from datetime import datetime


class QueueSystem:
    def __init__(self, root):
        self.preparing_queue = deque()
        self.finished_queue = deque()

        self.root = root
        self.root.title("Queue System")

        # Preparing Queue UI
        self.prep_label = tk.Label(root, text="Preparing Queue", font=("Arial", 14, "bold"))
        self.prep_label.grid(row=0, column=0, padx=10, pady=10)
        self.prep_listbox = tk.Listbox(root, width=30, height=10)
        self.prep_listbox.grid(row=1, column=0, padx=10, pady=10)
        self.add_button = tk.Button(root, text="Add Task", command=self.open_add_task_window)
        self.add_button.grid(row=2, column=0, padx=10, pady=10)

        # Finished Queue UI
        self.finished_label = tk.Label(root, text="Finished Queue", font=("Arial", 14, "bold"))
        self.finished_label.grid(row=0, column=1, padx=10, pady=10)
        self.finished_listbox = tk.Listbox(root, width=30, height=10)
        self.finished_listbox.grid(row=1, column=1, padx=10, pady=10)
        self.process_button = tk.Button(root, text="Process Task", command=self.open_process_window)
        self.process_button.grid(row=2, column=1, padx=10, pady=10)

    def open_add_task_window(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add Task")

        # Category Selection (BK / CS)
        tk.Label(self.add_window, text="Select Category:").pack(pady=5)
        self.category_var = tk.StringVar(self.add_window)
        self.category_var.set("BK")  # Default selection
        category_options = {"BK": "BK", "CS": "CS"}
        self.category_dropdown = tk.OptionMenu(self.add_window, self.category_var, *category_options.keys())
        self.category_dropdown.pack(pady=5)

        # Enter 2-digit number
        tk.Label(self.add_window, text="Enter 2-Digit Number:").pack(pady=5)
        self.prefix_entry = tk.Entry(self.add_window, width=5)
        self.prefix_entry.pack(pady=5)

        # Enter 3-digit number
        tk.Label(self.add_window, text="Enter 3-Digit Number:").pack(pady=5)
        self.number_entry = tk.Entry(self.add_window, width=5)
        self.number_entry.pack(pady=5)

        # Add Button
        tk.Button(self.add_window, text="Add",
                  command=lambda: self.add_task_from_window(category_options)).pack(pady=5)

    def add_task_from_window(self, category_options):
        category = self.category_var.get()
        prefix = self.prefix_entry.get()
        number = self.number_entry.get()

        # Validation: Ensure prefix is a 2-digit number and number is a 3-digit number
        if prefix.isdigit() and len(prefix) == 2 and number.isdigit() and len(number) == 3:
            full_task_name = f"{category}{prefix}/{number}"  # Format: CS23/456
            self.preparing_queue.append(full_task_name)
            self.prep_listbox.insert(tk.END, full_task_name)
            self.add_window.destroy()
        else:
            tk.Label(self.add_window, text="Invalid input! Enter a 2-digit and 3-digit number.", fg="red").pack()

    def open_process_window(self):
        if not self.preparing_queue:
            return

        self.process_window = tk.Toplevel(self.root)
        self.process_window.title("Select Task to Finish")

        tk.Label(self.process_window, text="Select a task to finish:").pack(pady=5)

        self.task_var = tk.StringVar(self.process_window)
        self.task_var.set(self.preparing_queue[0])  # Default selection
        self.task_dropdown = tk.OptionMenu(self.process_window, self.task_var, *self.preparing_queue)
        self.task_dropdown.pack(pady=5)

        tk.Button(self.process_window, text="Finish Task", command=self.finish_selected_task).pack(pady=5)

    def finish_selected_task(self):
        selected_task = self.task_var.get()
        if selected_task in self.preparing_queue:
            self.preparing_queue.remove(selected_task)
            self.finished_queue.append(selected_task)
            self.update_listboxes()
            self.process_window.destroy()

    def update_listboxes(self):
        self.prep_listbox.delete(0, tk.END)
        for task in self.preparing_queue:
            self.prep_listbox.insert(tk.END, task)

        self.finished_listbox.delete(0, tk.END)
        for task in self.finished_queue:
            self.finished_listbox.insert(tk.END, task)


if __name__ == "__main__":
    root = tk.Tk()
    app = QueueSystem(root)
    root.mainloop()

class QueueSystem:
    def __init__(self, root):
        self.preparing_queue = deque()
        self.finished_queue = deque()

        self.root = root
        self.root.title("Queue System")

        # Preparing Queue UI
        self.prep_label = tk.Label(root, text="Preparing Queue", font=("Arial", 14, "bold"))
        self.prep_label.grid(row=0, column=0, padx=10, pady=10)
        self.prep_listbox = tk.Listbox(root, width=30, height=10)
        self.prep_listbox.grid(row=1, column=0, padx=10, pady=10)
        self.add_button = tk.Button(root, text="Add Task", command=self.open_add_task_window)
        self.add_button.grid(row=2, column=0, padx=10, pady=10)

        # Finished Queue UI
        self.finished_label = tk.Label(root, text="Finished Queue", font=("Arial", 14, "bold"))
        self.finished_label.grid(row=0, column=1, padx=10, pady=10)
        self.finished_listbox = tk.Listbox(root, width=30, height=10)
        self.finished_listbox.grid(row=1, column=1, padx=10, pady=10)
        self.process_button = tk.Button(root, text="Process Task", command=self.open_process_window)
        self.process_button.grid(row=2, column=1, padx=10, pady=10)

    def open_add_task_window(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add Task")

        tk.Label(self.add_window, text="Select Category:").pack(pady=5)
        self.category_var = tk.StringVar(self.add_window)
        self.category_var.set("bk")  # Default selection
        category_options = {"bk": "bk", "cs": "cs"}
        self.category_dropdown = tk.OptionMenu(self.add_window, self.category_var, *category_options.keys())
        self.category_dropdown.pack(pady=5)

        tk.Label(self.add_window, text="Select Task Prefix:").pack(pady=5)
        self.task_var = tk.StringVar(self.add_window)
        self.task_var.set("pm")  # Default selection
        task_options = {"pm": "pm", "jn": "jn", "sm": "sm"}
        self.task_dropdown = tk.OptionMenu(self.add_window, self.task_var, *task_options.keys())
        self.task_dropdown.pack(pady=5)

        current_date = datetime.now().strftime("%Y%m")  # Format YYYYMMDD
        tk.Label(self.add_window, text=f"Date: {current_date}").pack(pady=5)

        tk.Label(self.add_window, text="Enter 4-Digit Number:").pack(pady=5)
        self.task_entry = tk.Entry(self.add_window, width=10)
        self.task_entry.pack(pady=5)

        tk.Button(self.add_window, text="Add",
                  command=lambda: self.add_task_from_window(category_options, task_options, current_date)).pack(pady=5)

    def add_task_from_window(self, category_options, task_options, current_date):
        category = self.category_var.get()
        prefix = self.task_var.get()
        number = self.task_entry.get()
        if len(number) == 4 and number.isdigit():
            full_task_name = f"{category_options[category]}{task_options[prefix]}{current_date}/{number}"
            self.preparing_queue.append(full_task_name)
            self.prep_listbox.insert(tk.END, full_task_name)
            self.add_window.destroy()
        else:
            tk.Label(self.add_window, text="Please enter a valid 4-digit number.", fg="red").pack()

    def open_process_window(self):
        if not self.preparing_queue:
            return

        self.process_window = tk.Toplevel(self.root)
        self.process_window.title("Select Task to Finish")

        tk.Label(self.process_window, text="Select a task to finish:").pack(pady=5)

        self.task_var = tk.StringVar(self.process_window)
        self.task_var.set(self.preparing_queue[0])  # Default selection
        self.task_dropdown = tk.OptionMenu(self.process_window, self.task_var, *self.preparing_queue)
        self.task_dropdown.pack(pady=5)

        tk.Button(self.process_window, text="Finish Task", command=self.finish_selected_task).pack(pady=5)

    def finish_selected_task(self):
        selected_task = self.task_var.get()
        if selected_task in self.preparing_queue:
            self.preparing_queue.remove(selected_task)
            self.finished_queue.append(selected_task)
            self.update_listboxes()
            self.process_window.destroy()

    def update_listboxes(self):
        self.prep_listbox.delete(0, tk.END)
        for task in self.preparing_queue:
            self.prep_listbox.insert(tk.END, task)

        self.finished_listbox.delete(0, tk.END)
        for task in self.finished_queue:
            self.finished_listbox.insert(tk.END, task)


if __name__ == "__main__":
    root = tk.Tk()
    app = QueueSystem(root)
    root.mainloop()
