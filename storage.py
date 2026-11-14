
"""File storage, CSV operations, backups, and activity logging."""

import csv
import json
import shutil
from pathlib import Path
from datetime import datetime

from models import Task


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = DATA_DIR / "backups"
EXPORT_DIR = BASE_DIR / "exports"

TASKS_FILE = DATA_DIR / "tasks.json"
LOG_FILE = DATA_DIR / "activity.log"


def ensure_folders():
    """Create the application's required folders."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def save_tasks(tasks):
    """Save all tasks to the JSON data file."""
    ensure_folders()

    data = [task.to_dict() for task in tasks]

    temporary_file = TASKS_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    temporary_file.replace(TASKS_FILE)


def load_tasks():
    """Load tasks from JSON and return an empty list if unavailable."""
    ensure_folders()

    if not TASKS_FILE.exists():
        return []

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("The task data must be a JSON list.")

        tasks = []

        for item in data:
            tasks.append(Task.from_dict(item))

        return tasks

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Could not load task data: {error}")
        print("Starting with an empty task list.")
        return []


def export_csv(tasks):
    """Export tasks to a CSV file and return its path."""
    ensure_folders()

    export_file = EXPORT_DIR / "tasks_export.csv"

    fieldnames = [
        "task_id",
        "title",
        "assignee",
        "priority",
        "due_date",
        "status",
        "created_at"
    ]

    with export_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for task in tasks:
            writer.writerow(task.to_dict())

    return export_file


def import_csv(path):
    """Import tasks from CSV and return valid Task objects."""
    imported_tasks = []

    csv_path = Path(path)

    with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                task = Task.from_dict({
                    "task_id": int(row["task_id"]),
                    "title": row["title"],
                    "assignee": row["assignee"],
                    "priority": row.get("priority") or "medium",
                    "due_date": row.get("due_date") or "",
                    "status": row.get("status") or "todo",
                    "created_at": row.get("created_at") or None
                })

                imported_tasks.append(task)

            except (ValueError, KeyError, TypeError) as error:
                print(f"Skipped an invalid CSV row: {error}")

    return imported_tasks


def backup_tasks():
    """Create a timestamped backup of the JSON task file."""
    ensure_folders()

    if not TASKS_FILE.exists():
        print("There is no saved task file to back up.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"tasks_backup_{timestamp}.json"

    shutil.copy2(TASKS_FILE, backup_file)

    return backup_file


def log_action(message):
    """Append a timestamped activity message to the log."""
    ensure_folders()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def read_log(n=20):
    """Return the most recent activity log entries."""
    ensure_folders()

    if not LOG_FILE.exists():
        return []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    return [line.rstrip("\n") for line in lines[-n:]]
