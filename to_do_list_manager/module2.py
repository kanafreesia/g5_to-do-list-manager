import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from to_do_list_manager.module1 import TodoList

class ToDoManager:
    def __init__(self, root):
        self.todo_list = TodoList()
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("550x400")
        self.root.configure(bg="#2C1A39")
        self.main_menu()

    def main_menu(self):
        self._clear_window()
        tk.Label(self.root, text="To-Do List Manager", font=("Arial", 20, "bold"), bg="#2C1A39", fg="white").pack(side=tk.TOP, pady=(20, 5))

        tk.Button(self.root, text="Add Task", command=self.add_task, width=20, height=2, bg="lightgreen").pack(pady=12)
        tk.Button(self.root, text="View Tasks", command=self.view_tasks, width=20, height=2, bg="lightgreen").pack(pady=12)
        tk.Button(self.root, text="Completed Tasks", command=self.completed_tasks, width=20, height=2, bg="lightgreen").pack(pady=12)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20, height=2, bg="lightgreen").pack(pady=12)

    def add_task(self):
        self._clear_window()
        tk.Label(self.root, text="Add Task", font=("Arial", 16), bg="#2C1A39", fg="white").pack(pady=10)

        tk.Label(self.root, text="Task Title:", bg="#2C1A39", fg="white").pack(pady=5)
        task_title_entry = tk.Entry(self.root, width=30)
        task_title_entry.pack(pady=5)

        tk.Label(self.root, text="Deadline (e.g., 2024-11-23):", bg="#2C1A39", fg="white").pack(pady=5)
        task_deadline_entry = tk.Entry(self.root, width=30)
        task_deadline_entry.pack(pady=5)

        tk.Label(self.root, text="Priority:", bg="#2C1A39", fg="white").pack(pady=5)
        priority_var = tk.StringVar(value="Medium")
        tk.OptionMenu(self.root, priority_var, "High", "Medium", "Low").pack(pady=5)

        def save_task():
            title = task_title_entry.get()
            deadline = task_deadline_entry.get()
            priority = priority_var.get()
            if not title:
                messagebox.showerror("Error", "Task title cannot be empty.")
                return

            if deadline:
                try:
                    datetime.strptime(deadline, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                    return

            self.todo_list.add_task(title, deadline, priority)
            messagebox.showinfo("Success", "Task added successfully.")
            self.main_menu()

        tk.Button(self.root, text="Save Task", command=save_task, bg="lightgreen").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu, bg="lightgreen").pack(pady=10)

    def view_tasks(self):
        self._clear_window()
        tk.Label(self.root, text="View Tasks", font=("Arial", 16), bg="#2C1A39", fg="white").pack(pady=10)

        tasks = self.todo_list.get_tasks(completed=False)

        if not tasks:
            tk.Label(self.root, text="No tasks found!", bg="#2C1A39", fg="white").pack(pady=10)
        else:
            tasks.sort(key=lambda t: ({"High": 1, "Medium": 2, "Low": 3}[t.priority], t.deadline or "9999-12-31"))

            for task in tasks:
                task_frame = tk.Frame(self.root, bg="#2C1A39")
                task_frame.pack(pady=5)

                task_text = f"{task.task} - Deadline: {task.deadline or 'None'}, Priority: {task.priority}"
                tk.Label(task_frame, text=task_text, bg="#2C1A39", fg="white").pack(side=tk.LEFT, padx=5)

                tk.Button(task_frame, text="Edit", command=lambda t=task: self.edit_task(t), bg="lightgreen").pack(side=tk.LEFT, padx=5)
                tk.Button(task_frame, text="Delete", command=lambda t=task: self.delete_task(t), bg="lightgreen").pack(side=tk.LEFT, padx=5)
                tk.Button(task_frame, text="Mark as Completed", command=lambda t=task: self.mark_completed(t), bg="lightgreen").pack(side=tk.LEFT, padx=5)

        tk.Button(self.root, text="Back", command=self.main_menu, bg="lightgreen").pack(pady=10)

    def edit_task(self, task):
        self._clear_window()
        tk.Label(self.root, text="Edit Task", font=("Arial", 16), bg="#2C1A39", fg="white").pack(pady=10)

        tk.Label(self.root, text="Task Title:", bg="#2C1A39", fg="white").pack(pady=5)
        task_title_entry = tk.Entry(self.root, width=30)
        task_title_entry.insert(0, task.task)
        task_title_entry.pack(pady=5)

        tk.Label(self.root, text="Deadline (YYYY-MM-DD):", bg="#2C1A39", fg="white").pack(pady=5)
        task_deadline_entry = tk.Entry(self.root, width=30)
        task_deadline_entry.insert(0, task.deadline or "")
        task_deadline_entry.pack(pady=5)

        tk.Label(self.root, text="Priority:", bg="#2C1A39", fg="white").pack(pady=5)
        priority_var = tk.StringVar(value=task.priority)
        tk.OptionMenu(self.root, priority_var, "High", "Medium", "Low").pack(pady=5)

        def save_task():
            title = task_title_entry.get()
            deadline = task_deadline_entry.get()
            priority = priority_var.get()

            if not title:
                messagebox.showerror("Error", "Task title cannot be empty.")
                return

            if deadline:
                try:
                    datetime.strptime(deadline, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                    return

            self.todo_list.edit_task(task, title, deadline, priority)
            messagebox.showinfo("Success", "Task updated successfully.")
            self.view_tasks()

        tk.Button(self.root, text="Save", command=save_task, bg="lightgreen").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.view_tasks, bg="lightgreen").pack(pady=10)

    def delete_task(self, task):
        self.todo_list.delete_task(task)
        messagebox.showinfo("Success", "Task deleted successfully.")
        self.view_tasks()

    def mark_completed(self, task):
        self.todo_list.mark_completed(task)
        messagebox.showinfo("Success", "Task marked as completed.")
        self.view_tasks()

    def completed_tasks(self):
        self._clear_window()
        tk.Label(self.root, text="Completed Tasks", font=("Arial", 16), bg="#2C1A39", fg="white").pack(pady=10)
        tasks = self.todo_list.get_tasks(completed=True)

        if not tasks:
            tk.Label(self.root, text="No completed tasks!", bg="#2C1A39", fg="white").pack(pady=10)
        else:
            for task in tasks:
                task_text = f"{task.task} - Deadline: {task.deadline or 'None'}, Priority: {task.priority}"
                tk.Label(self.root, text=task_text, bg="#2C1A39", fg="white").pack(pady=5)

        tk.Button(self.root, text="Back", command=self.main_menu, bg="lightgreen").pack(pady=10)

    def _clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()