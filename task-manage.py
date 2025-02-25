import json
import os
import logging
from datetime import datetime, timedelta
import random
import sqlite3
from dataclasses import dataclass
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db_file = "tasks.db"

@dataclass
class Task:
    id: int
    title: str
    due_date: str
    priority: str
    completed: bool = False
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    recurring: bool = False

class TaskManager:
    def __init__(self):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                due_date TEXT,
                                priority TEXT,
                                completed BOOLEAN,
                                created_at TEXT,
                                recurring BOOLEAN)''')
        self.conn.commit()

    def add_task(self, title, due_date, priority, recurring=False):
        self.cursor.execute("INSERT INTO tasks (title, due_date, priority, completed, created_at, recurring) VALUES (?, ?, ?, ?, ?, ?)",
                            (title, due_date, priority, False, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), recurring))
        self.conn.commit()
        logging.info("Task added successfully!")

    def edit_task(self, task_id, title=None, due_date=None, priority=None):
        updates = []
        params = []
        if title:
            updates.append("title = ?")
            params.append(title)
        if due_date:
            updates.append("due_date = ?")
            params.append(due_date)
        if priority:
            updates.append("priority = ?")
            params.append(priority)
        params.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, tuple(params))
        self.conn.commit()
        logging.info("Task updated successfully!")

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        logging.info("Task deleted successfully!")

    def list_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        if not tasks:
            logging.info("No tasks available.")
            return
        print("\nYour Tasks:")
        for task in tasks:
            status = "Completed" if task[4] else "Pending"
            recurring_status = " (Recurring)" if task[6] else ""
            print(f"{task[0]}. {task[1]} (Due: {task[2]}, Priority: {task[3]}, Status: {status}{recurring_status}, Created: {task[5]})")

    def mark_completed(self, task_id):
        self.cursor.execute("SELECT due_date, recurring FROM tasks WHERE id = ?", (task_id,))
        task = self.cursor.fetchone()
        if not task:
            logging.error("Task not found!")
            return
        if task[1]:
            new_due_date = (datetime.strptime(task[0], "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")
            self.cursor.execute("UPDATE tasks SET due_date = ?, completed = 0 WHERE id = ?", (new_due_date, task_id))
        else:
            self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        self.conn.commit()
        logging.info("Task marked as completed!")

    def search_tasks(self, keyword):
        self.cursor.execute("SELECT * FROM tasks WHERE title LIKE ?", (f"%{keyword}%",))
        tasks = self.cursor.fetchall()
        return tasks

    def generate_random_tasks(self, num):
        titles = ["Buy groceries", "Complete project", "Call client", "Schedule meeting", "Read a book"]
        priorities = ["High", "Medium", "Low"]
        for _ in range(num):
            title = random.choice(titles)
            due_date = (datetime.now().date()).strftime("%Y-%m-%d")
            priority = random.choice(priorities)
            self.add_task(title, due_date, priority)
        logging.info(f"{num} random tasks added successfully!")

    def menu(self):
        while True:
            print("\nTask Manager")
            print("1. Add Task")
            print("2. Edit Task")
            print("3. List Tasks")
            print("4. Delete Task")
            print("5. Mark Task as Completed")
            print("6. Search Task")
            print("7. Generate Random Tasks")
            print("8. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                title = input("Enter task title: ")
                due_date = input("Enter due date (YYYY-MM-DD): ")
                priority = input("Enter priority (High/Medium/Low): ")
                recurring = input("Is this a recurring task? (yes/no): ").lower() == "yes"
                self.add_task(title, due_date, priority, recurring)
            elif choice == "2":
                task_id = int(input("Enter task ID to edit: "))
                title = input("Enter new title (leave blank to keep unchanged): ") or None
                due_date = input("Enter new due date (YYYY-MM-DD) (leave blank to keep unchanged): ") or None
                priority = input("Enter new priority (High/Medium/Low) (leave blank to keep unchanged): ") or None
                self.edit_task(task_id, title, due_date, priority)
            elif choice == "3":
                self.list_tasks()
            elif choice == "4":
                task_id = int(input("Enter task ID to delete: "))
                self.delete_task(task_id)
            elif choice == "5":
                task_id = int(input("Enter task ID to mark as completed: "))
                self.mark_completed(task_id)
            elif choice == "6":
                keyword = input("Enter search keyword: ")
                tasks = self.search_tasks(keyword)
                for task in tasks:
                    print(f"{task[0]}. {task[1]} - Due: {task[2]}, Priority: {task[3]}, Completed: {task[4]}")
            elif choice == "7":
                num = int(input("Enter number of random tasks to generate: "))
                self.generate_random_tasks(num)
            elif choice == "8":
                logging.info("Exiting Task Manager. Goodbye!")
                break
            else:
                logging.warning("Invalid choice! Please try again.")

if __name__ == "__main__":
    manager = TaskManager()
    manager.menu()