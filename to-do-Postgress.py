import psycopg2
import tkinter as tk
from tkinter import messagebox

def connect_to_db():
    return psycopg2.connect(
        host="db-postgresql-nyc1-14277-do-user-18417666-0.g.db.ondigitalocean.com",
        port=25060,
        user="doadmin",
        password="AVNS_GmPWKRB8Tjatu14QzT7",
        database="defaultdb"
    )

def create_user_table(user_name):
    with connect_to_db() as db:
        with db.cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS "{user_name}" (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    status BOOLEAN DEFAULT FALSE
                )
            """)
            db.commit()

def display_tasks(user_name, listbox):
    with connect_to_db() as db:
        with db.cursor() as cursor:
            cursor.execute(f'SELECT * FROM "{user_name}"')
            tasks = cursor.fetchall()

    listbox.delete(0, tk.END)
    for task in tasks:
        status = "Done" if task[3] else "Not Done"
        listbox.insert(tk.END, f"{task[0]}. {task[1]} - {task[2]} [{status}]")

def add_task(user_name, title, description):
    with connect_to_db() as db:
        with db.cursor() as cursor:
            cursor.execute(f'INSERT INTO "{user_name}" (title, description) VALUES (%s, %s)', (title, description))
            db.commit()
    messagebox.showinfo("Success", "Task added successfully!")

def remove_task(user_name, task_id):
    with connect_to_db() as db:
        with db.cursor() as cursor:
            cursor.execute(f'DELETE FROM "{user_name}" WHERE id = %s', (task_id,))
            db.commit()
    messagebox.showinfo("Success", "Task removed successfully!")

def mark_task_completed(user_name, task_id):
    with connect_to_db() as db:
        with db.cursor() as cursor:
            cursor.execute(f'UPDATE "{user_name}" SET status = TRUE WHERE id = %s', (task_id,))
            db.commit()
    messagebox.showinfo("Success", "Task marked as completed!")

def main():
    root = tk.Tk()
    root.title("To-Do List Application")

    tk.Label(root, text="Enter your name without any space:").pack(pady=5)
    user_name_entry = tk.Entry(root)
    user_name_entry.pack(pady=5)

    def start_app():
        user_name = user_name_entry.get().strip()
        if not user_name:
            messagebox.showerror("Error", "User name is required!")
            return

        create_user_table(user_name)

        for widget in root.winfo_children():
            widget.destroy()

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
                try:
                    task_id = int(task_id)
                    remove_task(user_name, task_id)
                    refresh_tasks()
                except ValueError:
                    messagebox.showerror("Error", "Invalid task selected!")

        def mark_task_completed_gui():
            selected_task = listbox.get(tk.ACTIVE)
            if selected_task:
                task_id = selected_task.split(".")[0]
                try:
                    task_id = int(task_id)
                    mark_task_completed(user_name, task_id)
                    refresh_tasks()
                except ValueError:
                    messagebox.showerror("Error", "Invalid task selected!")

        tk.Label(root, text="Task Title:").pack(pady=5)
        task_title_entry = tk.Entry(root, width=40)
        task_title_entry.pack(pady=5)

        tk.Label(root, text="Task Description:").pack(pady=5)
        task_description_entry = tk.Entry(root, width=40)
        task_description_entry.pack(pady=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Task", command=add_task_gui).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Remove Task", command=remove_task_gui).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Mark as Done", command=mark_task_completed_gui).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Refresh", command=refresh_tasks).grid(row=0, column=3, padx=5)

        refresh_tasks()

    tk.Button(root, text="Start", command=start_app).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
