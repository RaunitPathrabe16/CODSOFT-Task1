import os
import tkinter as tk
from tkinter import ttk, messagebox
import json

class TodoTrek:
    def __init__(self, root):
        self.root = root
        self.root.title("TodoTrek List")
        self.root.geometry("500x650")
        self.root.configure(bg="#3b9dd1")

        # Set up styles
        style = ttk.Style()
        style.theme_use("clam")  # Use a valid theme name
        style.configure("TFrame", background="#3b9dd1")
        style.configure("TButton", padding=6, font=('Open Sans', 12), background="#ffffff")
        style.configure("TEntry", padding=6, font=('Open Sans', 12))
        style.configure("Treeview", font=('Open Sans', 12), rowheight=25, fieldbackground="#f5f5f5")
        style.configure("Treeview.Heading", font=('Open Sans', 13, 'bold'))

        # Main frame
        self.frame = ttk.Frame(self.root, padding="12")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Task entry field
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(self.frame, textvariable=self.task_var, width=40)
        self.task_entry.grid(row=0, column=0, padx=5, pady=10, sticky='ew')

        # Buttons for adding and updating tasks
        self.add_button = ttk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=5, pady=10)

        self.update_button = ttk.Button(self.frame, text="Update Task", command=self.update_task)
        self.update_button.grid(row=0, column=2, padx=5, pady=10)

        # Treeview for task list
        self.task_tree = ttk.Treeview(self.frame, columns=("Task"), show="headings", selectmode="browse")
        self.task_tree.heading("Task", text="Task List")
        self.task_tree.column("Task", width=350, anchor="w")
        self.task_tree.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky='nsew')

        # Scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=3, sticky='ns')

        # Buttons for deleting and saving tasks
        self.delete_button = ttk.Button(self.frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=5, pady=10, sticky='ew')

        self.save_button = ttk.Button(self.frame, text="Save Tasks", command=self.save_tasks)
        self.save_button.grid(row=2, column=1, padx=5, pady=10, sticky='ew')

        self.load_button = ttk.Button(self.frame, text="Load Tasks", command=self.load_tasks)
        self.load_button.grid(row=2, column=2, padx=5, pady=10, sticky='ew')

        # Configure grid weight
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            self.task_tree.insert("", tk.END, values=(task,))
            self.task_var.set("")
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def update_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task = self.task_var.get().strip()
            if task:
                self.task_tree.item(selected_item, values=(task,))
                self.task_var.set("")
            else:
                messagebox.showwarning("Warning", "Please enter a task to update.")
        else:
            messagebox.showerror("Error", "Please select a task to update.")

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            for item in selected_item:
                self.task_tree.delete(item)
        else:
            messagebox.showerror("Warning", "Please select a task to delete.")

    def save_tasks(self):
        tasks = [self.task_tree.item(child)['values'][0] for child in self.task_tree.get_children()]
        with open("tasks.json", "w") as f:
            json.dump(tasks, f)
        messagebox.showinfo("Info", "Tasks saved successfully.")

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
            self.task_tree.delete(*self.task_tree.get_children())
            for task in tasks:
                self.task_tree.insert("", tk.END, values=(task,))
        else:
            messagebox.showwarning("Warning", "No saved tasks found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoTrek(root)
    root.mainloop()
