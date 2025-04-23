import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import threading
import datetime
import time

TASK_FILE = "tasks.txt"

# Function to add a new task
def add_task():
    task = task_entry.get()
    if task != "":
        tasks_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Function to add a task with a reminder
def add_task_with_reminder():
    task = task_entry.get()
    if task == "":
        messagebox.showwarning("Input Error", "Please enter a task first.")
        return

    time_str = simpledialog.askstring("Set Reminder", "Enter time in HH:MM (24hr) format:")
    try:
        reminder_time = datetime.datetime.strptime(time_str, "%H:%M").time()
        now = datetime.datetime.now()
        reminder_datetime = datetime.datetime.combine(now.date(), reminder_time)

        if reminder_datetime < now:
            reminder_datetime += datetime.timedelta(days=1)

        tasks_listbox.insert(tk.END, f"{task} (Reminder at {reminder_time.strftime('%H:%M')})")
        task_entry.delete(0, tk.END)

        threading.Thread(target=schedule_reminder, args=(task, reminder_datetime), daemon=True).start()
    except Exception:
        messagebox.showerror("Time Format Error", "Please enter time in HH:MM format.")

# Function to schedule a reminder
def schedule_reminder(task, remind_at):
    while True:
        if datetime.datetime.now() >= remind_at:
            messagebox.showinfo("Reminder", f"Time for: {task}")
            break
        time.sleep(30)

# Function to delete selected task
def delete_task():
    try:
        selected_index = tasks_listbox.curselection()[0]
        tasks_listbox.delete(selected_index)
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Function to edit selected task
def edit_task():
    try:
        selected_index = tasks_listbox.curselection()[0]
        old_task = tasks_listbox.get(selected_index)
        new_task = simpledialog.askstring("Edit Task", "Edit the selected task:", initialvalue=old_task)
        if new_task and new_task.strip() != "":
            tasks_listbox.delete(selected_index)
            tasks_listbox.insert(selected_index, new_task.strip())
        else:
            messagebox.showinfo("Edit Cancelled", "No changes were made.")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")

# Function to save tasks to a file
def save_tasks():
    tasks = tasks_listbox.get(0, tk.END)
    with open(TASK_FILE, "w") as file:
        for task in tasks:
            file.write(task + "\n")
    messagebox.showinfo("Save Successful", f"Tasks saved to '{TASK_FILE}'.")

# Function to load tasks from a file
def load_tasks():
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, "w") as file:
            pass
        messagebox.showinfo("File Created", f"Created new file '{TASK_FILE}'.")
        return

    with open(TASK_FILE, "r") as file:
        for line in file:
            tasks_listbox.insert(tk.END, line.strip())

# GUI setup
root = tk.Tk()
root.title("To-Do List with Edit & Reminders")
root.geometry("400x550")

task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

# Buttons
add_button = tk.Button(root, text="Add Task", width=20, command=add_task)
add_button.pack(pady=5)

reminder_button = tk.Button(root, text="Add Task with Reminder", width=20, command=add_task_with_reminder)
reminder_button.pack(pady=5)

edit_button = tk.Button(root, text="Edit Task", width=20, command=edit_task)
edit_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", width=20, command=delete_task)
delete_button.pack(pady=5)

save_button = tk.Button(root, text="Save Tasks", width=20, command=save_tasks)
save_button.pack(pady=5)

tasks_listbox = tk.Listbox(root, width=50, height=15)
tasks_listbox.pack(pady=10)

# Load existing tasks
load_tasks()

# Start the app
root.mainloop()