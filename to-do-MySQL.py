import mysql.connector
import tkinter as tk
from tkinter import messagebox

# MySQL Database Connection
def connect_to_db():
    return mysql.connector.connect(
        host="host",
        port=port,  # Use the correct port for MySQL
        user="username",  # Replace with your MySQL username
        password="password",  # Replace with your MySQL password
        database="datbase"
    )

# Function to create a table for the user
def create_user_table(user_name):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {user_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status BOOLEAN DEFAULT FALSE
        )
    """)
    db.commit()
    db.close()

# Function to display all tasks
def display_tasks(user_name, listbox):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {user_name}")
    tasks = cursor.fetchall()
    db.close()

    listbox.delete(0, tk.END)
    for task in tasks:
        status = "Done" if task[3] else "Not Done"
        listbox.insert(tk.END, f"{task[0]}. {task[1]} - {task[2]} [{status}]")

# Function to add a new task
def add_task(user_name, title, description):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO {user_name} (title, description) VALUES (%s, %s)", (title, description))
    db.commit()
    db.close()
    messagebox.showinfo("Success", "Task added successfully!")

# Function to remove a task
def remove_task(user_name, task_id):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM {user_name} WHERE id = %s", (task_id,))
    db.commit()
    db.close()
    messagebox.showinfo("Success", "Task removed successfully!")

# Function to mark a task as completed
def mark_task_completed(user_name, task_id):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute(f"UPDATE {user_name} SET status = TRUE WHERE id = %s", (task_id,))
    db.commit()
    db.close()
    messagebox.showinfo("Success", "Task marked as completed!")

# Main Application GUI
def main():
    root = tk.Tk()
    root.title("To-Do List Application")

    # Get user name directly in the main window
    tk.Label(root, text="Enter your name:").pack(pady=5)
    user_name_entry = tk.Entry(root)
    user_name_entry.pack(pady=5)

    def start_app():
        user_name = user_name_entry.get().strip()
        if not user_name:
            messagebox.showerror("Error", "User name is required!")
            return

        create_user_table(user_name)

        # Clear the main window
        for widget in root.winfo_children():
            widget.destroy()

        # GUI Elements
        frame = tk.Frame(root)
        frame.pack(pady=10)

        listbox = tk.Listbox(frame, width=50, height=15)
        listbox.pack(side=tk.LEFT, padx=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        def refresh_tasks():
            display_tasks(user_name, listbox)

        def add_task_gui():
            title = task_title_entry.get().strip()
            description = task_description_entry.get().strip()
            if title:
                add_task(user_name, title, description)
                refresh_tasks()
                task_title_entry.delete(0, tk.END)
                task_description_entry.delete(0, tk.END)

        def remove_task_gui():
            selected_task = listbox.get(tk.ACTIVE)
            if selected_task:
                task_id = selected_task.split(".")[0]
                remove_task(user_name, task_id)
                refresh_tasks()

        def mark_task_completed_gui():
            selected_task = listbox.get(tk.ACTIVE)
            if selected_task:
                task_id = selected_task.split(".")[0]
                mark_task_completed(user_name, task_id)
                refresh_tasks()

        # Task Input Fields
        tk.Label(root, text="Task Title:").pack(pady=5)
        task_title_entry = tk.Entry(root, width=40)
        task_title_entry.pack(pady=5)

        tk.Label(root, text="Task Description:").pack(pady=5)
        task_description_entry = tk.Entry(root, width=40)
        task_description_entry.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add Task", command=add_task_gui)
        add_button.grid(row=0, column=0, padx=5)

        remove_button = tk.Button(button_frame, text="Remove Task", command=remove_task_gui)
        remove_button.grid(row=0, column=1, padx=5)

        mark_button = tk.Button(button_frame, text="Mark as Done", command=mark_task_completed_gui)
        mark_button.grid(row=0, column=2, padx=5)

        refresh_button = tk.Button(button_frame, text="Refresh", command=refresh_tasks)
        refresh_button.grid(row=0, column=3, padx=5)

        refresh_tasks()

    tk.Button(root, text="Start", command=start_app).pack(pady=10)

    root.mainloop()

# Run the application
if __name__ == "__main__":
    main()
