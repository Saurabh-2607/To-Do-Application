# To-Do List Application

This repository contains two implementations of a GUI-based To-Do List application using the Tkinter library in Python:
1. PostgreSQL-based implementation
2. MySQL-based implementation

## Features
- Add tasks with a title and description
- View all tasks in a list with their status (Done/Not Done)
- Mark tasks as completed
- Remove tasks
- Persistent storage of tasks using PostgreSQL or MySQL databases

## Dependencies

### Python Libraries:
- `psycopg2` (for PostgreSQL)
- `mysql-connector` (for MySQL)
- `tkinter` (for GUI)

Install required libraries:
```bash
pip install psycopg2 mysql-connector-python
```

### PostgreSQL Setup
- Replace the connection details in `connect_to_db` with your PostgreSQL credentials:
```python
return psycopg2.connect(
    host="<host>",
    port=<port>,
    user="<username>",
    password="<password>",
    database="<database>"
)
```
- Ensure your PostgreSQL server allows connections from your application.

### MySQL Setup
- Replace the connection details in `connect_to_db` with your MySQL credentials:
```python
return mysql.connector.connect(
    host="<host>",
    port=<port>,
    user="<username>",
    password="<password>",
    database="<database>"
)
```
- Ensure your MySQL server allows connections from your application.

## Usage

### Common Instructions
1. Run the application using Python:
   ```bash
   python <filename>.py
   ```
2. Enter a username to create or access a user-specific table for tasks.
3. Use the GUI to add, view, remove, or mark tasks as done.

### PostgreSQL Implementation
Run the file containing the PostgreSQL implementation. Example:
```bash
python todo_postgresql.py
```

### MySQL Implementation
Run the file containing the MySQL implementation. Example:
```bash
python todo_mysql.py
```

### Create an Executable File
To create a standalone `.exe` file for the application, use `pyinstaller`:

1. Install `pyinstaller`:
   ```bash
   pip install pyinstaller
   ```

2. Generate the `.exe` file:
   ```bash
   pyinstaller --onefile --windowed <filename>.py
   ```

   - `--onefile`: Creates a single executable file.
   - `--windowed`: Hides the console window (useful for GUI applications).

3. The `.exe` file will be located in the `dist` folder.

## Security Note
Make sure to replace hardcoded credentials with environment variables or a secure configuration file. Never expose your credentials in production environments.

## Improvements
1. **Authentication**: Add a login/signup system to manage user accounts.
2. **Search/Filter**: Enable search or filter tasks by status.
3. **Cross-Database Compatibility**: Allow the user to choose between PostgreSQL and MySQL at runtime.
4. **Styling**: Improve the GUI design with additional libraries like `ttk` or `customtkinter`.

## License
This project is open-source and free to use under the MIT License.
