import tkinter as tk
from tkinter import messagebox
import json

try:
    with open("tasks.json", "r") as file:
        tasks = json.load(file)

except (FileNotFoundError, json.JSONDecodeError):
    tasks = []

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)


def update_listbox():
    listbox.delete(0, tk.END)
    for i, task in enumerate(tasks, start=1):
        status = "✓" if task["completed"] else " "
        text = f"{i}. [{status}] {task['title']} | Priority: {task['priority']}"
        listbox.insert(tk.END, text)


def add_task():
    title = entry.get().strip()
    priority = priority_var.get()
    if title == "":
        messagebox.showwarning("Warning", "Please enter a task.")
        return

    task = { "title": title, "completed": False, "priority": priority
    }

    tasks.append(task)
    save_tasks()
    update_listbox()
    entry.delete(0, tk.END)


def delete_task():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task.")
        return
    
    index = selected[0]
    tasks.pop(index)
    save_tasks()
    update_listbox()


def toggle_complete():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task.")
        return
    
    index = selected[0]
    tasks[index]["completed"] = not tasks[index]["completed"]
    save_tasks()
    update_listbox()


def edit_task():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task.")
        return

    index = selected[0]
    new_title = entry.get().strip()
    new_priority = priority_var.get()
    if new_title == "":
        messagebox.showwarning("Warning", "Enter updated task.")
        return

    tasks[index]["title"] = new_title
    tasks[index]["priority"] = new_priority
    save_tasks()
    update_listbox()
    entry.delete(0, tk.END)


def load_selected_task(event):
    selected = listbox.curselection()

    if selected:
        index = selected[0]
        entry.delete(0, tk.END)
        entry.insert(0, tasks[index]["title"])
        priority_var.set(tasks[index]["priority"])


window = tk.Tk()
window.title("To-Do List App")
window.geometry("600x500")
window.configure(bg="black")

heading = tk.Label( window, text="To-Do List", font=("Ghost Danger", 20, "bold"), bg="black", fg="white")
heading.pack(pady=15)

entry = tk.Entry(window, width=35, font=("Arial", 12))
entry.pack(pady=10)

priority_var = tk.StringVar()
priority_var.set("Medium")
priority_menu = tk.OptionMenu(window, priority_var, "High", "Medium", "Low")
priority_menu.pack(pady=5)

button_frame = tk.Frame(window, bg="black")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Task", width=15, command=add_task)
add_button.grid(row=0, column=0, padx=5, pady=5)

edit_button = tk.Button(button_frame, text="Edit Task", width=15, command=edit_task)
edit_button.grid(row=0, column=1, padx=5, pady=5)

complete_button = tk.Button(button_frame, text="Complete / Undo", width=15, command=toggle_complete)
complete_button.grid(row=1, column=0, padx=5, pady=5)

delete_button = tk.Button(button_frame, text="Delete Task", width=15, command=delete_task)
delete_button.grid(row=1, column=1, padx=5, pady=5)

listbox = tk.Listbox(window, width=60, height=15, font=("Arial", 11))
listbox.pack(pady=15)
listbox.bind("<<ListboxSelect>>", load_selected_task)

update_listbox()
window.mainloop()
