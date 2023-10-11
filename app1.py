import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("todo.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        complete INTEGER,
        due_date DATE
    )
""")
conn.commit()

root = tk.Tk()
root.title("To-Do App")

# Function to create a new task
def create_task():
    task = task_entry.get()
    if task:
        cursor.execute("INSERT INTO tasks (task, complete) VALUES (?, ?)", (task, 0))
        conn.commit()
        update_task_list()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty")

# Function to read tasks from the database
def read_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

# Function to update the task list in the GUI
def update_task_list():
    task_list.delete(0, tk.END)
    for task in read_tasks():
        task_list.insert(tk.END, f"{task[1]} - {'Complete' if task[2] == 1 else 'Not Complete'}")

# Function to mark a task as complete or not complete
def toggle_task():
    selected_task = task_list.get(tk.ACTIVE)
    if selected_task:
        task_name = selected_task.split(" - ")[0]
        cursor.execute("SELECT complete FROM tasks WHERE task=?", (task_name,))
        current_status = cursor.fetchone()[0]
        new_status = 1 if current_status == 0 else 0
        cursor.execute("UPDATE tasks SET complete=? WHERE task=?", (new_status, task_name))
        conn.commit()
        update_task_list()

# Function to delete a task
def delete_task():
    selected_task = task_list.get(tk.ACTIVE)
    if selected_task:
        task_name = selected_task.split(" - ")[0]
        cursor.execute("DELETE FROM tasks WHERE task=?", (task_name,))
        conn.commit()
        update_task_list()

task_label = tk.Label(root, text="Task:")
task_label.pack()
task_entry = tk.Entry(root)
task_entry.pack()

create_button = tk.Button(root, text="Add Task", command=create_task)
create_button.pack()

task_list = tk.Listbox(root, width=50)
task_list.pack()

mark_complete_button = tk.Button(root, text="Mark Complete/Not Complete", command=toggle_task)
mark_complete_button.pack()

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack()

update_task_list()

root.mainloop()
