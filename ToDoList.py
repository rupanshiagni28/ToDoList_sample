import tkinter as tk
import mysql.connector
from tkinter import messagebox

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anshika79855@",
    database="todolist"
)

mycursor = mydb.cursor()

# Create tasks table if not exists
mycursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255), completed BOOLEAN)")


#FUNCTIONS
def add_task():
    task = entry_task.get()
    if task != "":
        sql = "INSERT INTO tasks (task, completed) VALUES (%s, %s)"
        val = (task, False)
        mycursor.execute(sql, val)
        mydb.commit()
        list_tasks()
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

def remove_task():
    try:
        index = listbox_tasks.curselection()[0]
        task_id = listbox_tasks.get(index).split(":")[0]
        sql = "DELETE FROM tasks WHERE id = %s"
        val = (task_id,)
        mycursor.execute(sql, val)
        mydb.commit()
        list_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove.")

def mark_as_completed():
    try:
        index = listbox_tasks.curselection()[0]
        task_id = listbox_tasks.get(index).split(":")[0]
        sql = "UPDATE tasks SET completed = True WHERE id = %s"
        val = (task_id,)
        mycursor.execute(sql, val)
        mydb.commit()
        list_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as completed.")

def mark_as_uncompleted():
    try:
        index = listbox_tasks.curselection()[0]
        task_id = listbox_tasks.get(index).split(":")[0]
        sql = "UPDATE tasks SET completed = False WHERE id = %s"
        val = (task_id,)
        mycursor.execute(sql, val)
        mydb.commit()
        list_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as uncompleted.")

def update_task():
    try:
        index = listbox_tasks.curselection()[0]
        task_id = listbox_tasks.get(index).split(":")[0]
        updated_task = entry_task.get()
        if updated_task != "":
            sql = "UPDATE tasks SET task = %s WHERE id = %s"
            val = (updated_task, task_id)
            mycursor.execute(sql, val)
            mydb.commit()
            list_tasks()
            entry_task.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to update.")

def list_tasks():
    listbox_tasks.delete(0, tk.END)
    mycursor.execute("SELECT * FROM tasks")
    tasks = mycursor.fetchall()
    for task in tasks:
        task_id, task_desc, completed = task
        status = "Completed" if completed else "Uncompleted"
        listbox_tasks.insert(tk.END, f"{task_id}: {task_desc} ({status})")

root = tk.Tk()
root.title("To-Do List")
root.resizable(False,False)

# FRAME_WIDGET
frame_tasks = tk.Frame(root)
frame_tasks.pack()

listbox_tasks = tk.Listbox(frame_tasks, height=10, width=50, bg="light grey")
listbox_tasks.pack(side=tk.LEFT)

scrollbar_tasks = tk.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)

listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

#ENTRY_WIDGET
entry_task = tk.Entry(root, width=40)
entry_task.pack()

#BUTTON_WIDGET
button_add_task = tk.Button(root, text="Add Task", width=48, command=add_task)
button_add_task.pack()

button_remove_task = tk.Button(root, text="Remove Task", width=48, command=remove_task)
button_remove_task.pack()

button_mark_completed = tk.Button(root, text="Mark as Completed", width=48, command=mark_as_completed)
button_mark_completed.pack()

button_mark_uncompleted = tk.Button(root, text="Mark as Uncompleted", width=48, command=mark_as_uncompleted)
button_mark_uncompleted.pack()

button_update_task = tk.Button(root, text="Update Task", width=48, command=update_task)
button_update_task.pack()

list_tasks()  # Populate the listbox with existing tasks from the database

root.mainloop()
