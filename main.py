
"""Main entry point for the TaskFlow application."""

from pathlib import Path

from utils import (
    print_header,
    ask_text,
    ask_choice,
    ask_date,
    ask_int,
    VALID_PRIORITIES,
    VALID_STATUSES
)

from manager import TaskManager

from storage import (
    ensure_folders,
    load_tasks,
    save_tasks,
    export_csv,
    import_csv,
    backup_tasks,
    log_action,
    read_log
)

from reports import build_report_text, save_report


def add_task_flow(manager):
    """Collect task details and add a new task."""
    print_header("ADD NEW TASK")

    title = ask_text("Task title: ")
    assignee = ask_text("Assigned to: ")

    priority = ask_choice(
        "Priority (low/medium/high) [medium]: ",
        VALID_PRIORITIES,
        default="medium"
    )

    due_date = ask_date(
        "Due date (YYYY-MM-DD), press Enter to skip: "
    )

    try:
        task = manager.add_task(
            title,
            assignee,
            priority,
            due_date
        )

        save_tasks(manager.tasks)
        log_action(f"Added task #{task.task_id}: {task.title}")

        print(f"\nTask #{task.task_id} added successfully.")

    except ValueError as error:
        print(f"Could not add task: {error}")


def show_tasks(tasks):
    """Display a list of tasks in a readable format."""
    print_header("TASK LIST")

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        overdue_label = " | OVERDUE" if task.is_overdue() else ""
        print(f"{task}{overdue_label}")


def filter_tasks_flow(manager):
    """Allow the user to filter tasks by different fields."""
    print_header("FILTER TASKS")

    print("1. Filter by assignee")
    print("2. Filter by status")
    print("3. Filter by priority")
    print("4. Combine filters")

    choice = ask_choice("Choose filter: ", ("1", "2", "3", "4"))

    assignee = None
    status = None
    priority = None

    if choice in ("1", "4"):
        assignee = ask_text(
            "Enter assignee name: "
        )

    if choice in ("2", "4"):
        status = ask_choice(
            "Status (todo/in_progress/done): ",
            VALID_STATUSES
        )

    if choice in ("3", "4"):
        priority = ask_choice(
            "Priority (low/medium/high): ",
            VALID_PRIORITIES
        )

    results = manager.filter_tasks(
        assignee=assignee,
        status=status,
        priority=priority
    )

    show_tasks(results)


def search_tasks_flow(manager):
    """Search for tasks using a title or assignee keyword."""
    print_header("SEARCH TASKS")

    keyword = ask_text("Enter search keyword: ")
    results = manager.search(keyword)

    show_tasks(results)


def change_status_flow(manager):
    """Change the status of an existing task."""
    print_header("UPDATE TASK STATUS")

    task_id = ask_int("Enter task ID: ")

    task = manager.find_by_id(task_id)

    if task is None:
        print("Task not found.")
        return

    print(f"Selected task: {task}")

    new_status = ask_choice(
        "New status (todo/in_progress/done): ",
        VALID_STATUSES
    )

    if manager.change_status(task_id, new_status):
        save_tasks(manager.tasks)
        log_action(
            f"Changed task #{task_id} status to {new_status}"
        )
        print("Task status updated successfully.")
    else:
        print("Unable to update task.")


def delete_task_flow(manager):
    """Delete a task after asking for confirmation."""
    print_header("DELETE TASK")

    task_id = ask_int("Enter task ID: ")
    task = manager.find_by_id(task_id)

    if task is None:
        print("Task not found.")
        return

    print(f"Selected task: {task}")

    confirmation = ask_choice(
        "Are you sure you want to delete it? (yes/no): ",
        ("yes", "no")
    )

    if confirmation == "yes":
        manager.delete_task(task_id)
        save_tasks(manager.tasks)
        log_action(f"Deleted task #{task_id}")
        print("Task deleted successfully.")
    else:
        print("Deletion cancelled.")


def show_overdue_tasks(manager):
    """Display all tasks that have passed their due dates."""
    print_header("OVERDUE TASKS")

    overdue = manager.overdue_tasks()
    show_tasks(overdue)


def show_statistics(manager):
    """Display overall task statistics and assignee totals."""
    print_header("TASK STATISTICS")

    statistics = manager.stats()

    print(f"Total tasks: {statistics['total']}")
    print(f"Completed: {statistics['completed']}")
    print(f"In progress: {statistics['in_progress']}")
    print(f"Pending: {statistics['pending']}")
    print(f"Overdue: {statistics['overdue']}")

    print("\nTASKS PER ASSIGNEE")
    print("-" * 40)

    counts = manager.tasks_per_assignee()

    if not counts:
        print("No assigned tasks.")
    else:
        for person, count in sorted(counts.items()):
            print(f"{person}: {count}")


def export_tasks_flow(manager):
    """Export the current tasks to a CSV file."""
    print_header("EXPORT TASKS")

    export_file = export_csv(manager.tasks)

    print(f"Tasks exported successfully to:\n{export_file}")


def import_tasks_flow(manager):
    """Import tasks from a CSV file and assign new unique IDs."""
    print_header("IMPORT TASKS")

    path_text = ask_text("Enter CSV file path: ")
    csv_path = Path(path_text).expanduser()

    if not csv_path.is_file():
        print("The specified file does not exist.")
        return

    try:
        imported = import_csv(csv_path)

        if not imported:
            print("No valid tasks were found in the CSV file.")
            return

        added_count = 0

        for imported_task in imported:
            try:
                manager.add_task(
                    title=imported_task.title,
                    assignee=imported_task.assignee,
                    priority=imported_task.priority,
                    due_date=imported_task.due_date
                )

                new_task = manager.tasks[-1]
                new_task.status = imported_task.status
                new_task.created_at = imported_task.created_at
                added_count += 1

            except ValueError as error:
                print(f"Skipped task: {error}")

        save_tasks(manager.tasks)
        log_action(f"Imported {added_count} tasks from CSV")

        print(f"Successfully imported {added_count} tasks.")

    except (OSError, UnicodeError, ValueError) as error:
        print(f"Could not import CSV: {error}")


def create_backup_flow():
    """Create a backup of the current saved task data."""
    print_header("CREATE BACKUP")

    backup_file = backup_tasks()

    if backup_file:
        print(f"Backup created successfully:\n{backup_file}")


def show_activity_log():
    """Display recent activity log entries."""
    print_header("ACTIVITY LOG")

    number = ask_int("How many recent entries? ", minimum=1)
    entries = read_log(number)

    if not entries:
        print("No activity has been recorded yet.")
        return

    for entry in entries:
        print(entry)


def generate_report(manager):
    """Generate and save a text report of the current tasks."""
    print_header("GENERATE REPORT")

    report_text = build_report_text(
        manager.tasks,
        manager.stats()
    )

    report_file = save_report(report_text)

    print(report_text)
    print(f"\nReport saved to:\n{report_file}")


def display_menu():
    """Display the main TaskFlow menu."""
    print_header("TASKFLOW - TEAM TASK MANAGEMENT SYSTEM")

    print("1.  Add a task")
    print("2.  List all tasks")
    print("3.  List tasks by priority")
    print("4.  Filter tasks")
    print("5.  Search tasks")
    print("6.  Update task status")
    print("7.  Delete a task")
    print("8.  View overdue tasks")
    print("9.  View statistics")
    print("10. Export tasks to CSV")
    print("11. Import tasks from CSV")
    print("12. Create a backup")
    print("13. View activity log")
    print("14. Generate text report")
    print("0.  Save and exit")


def main():
    """Load saved tasks and run the TaskFlow application."""
    ensure_folders()

    manager = TaskManager(load_tasks())

    print_header("WELCOME TO TASKFLOW")
    print("Your team's work, organised in one place.")

    while True:
        display_menu()

        choice = ask_choice(
            "\nChoose an option: ",
            tuple(str(number) for number in range(15))
        )

        if choice == "1":
            add_task_flow(manager)

        elif choice == "2":
            show_tasks(manager.tasks)

        elif choice == "3":
            show_tasks(manager.sorted_by_priority())

        elif choice == "4":
            filter_tasks_flow(manager)

        elif choice == "5":
            search_tasks_flow(manager)

        elif choice == "6":
            change_status_flow(manager)

        elif choice == "7":
            delete_task_flow(manager)

        elif choice == "8":
            show_overdue_tasks(manager)

        elif choice == "9":
            show_statistics(manager)

        elif choice == "10":
            export_tasks_flow(manager)

        elif choice == "11":
            import_tasks_flow(manager)

        elif choice == "12":
            create_backup_flow()

        elif choice == "13":
            show_activity_log()

        elif choice == "14":
            generate_report(manager)

        elif choice == "0":
            save_tasks(manager.tasks)
            log_action("Application closed and tasks saved.")

            print("\nAll tasks saved successfully.")
            print("Thank you for using TaskFlow.")
            break


if __name__ == "__main__":
    main()
