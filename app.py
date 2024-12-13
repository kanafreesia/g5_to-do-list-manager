import tkinter as tk
from to_do_list_manager.module2 import ToDoManager

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoManager(root)
    root.mainloop()
