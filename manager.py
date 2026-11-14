
"""Task manager containing the application's business logic."""

from models import Task
from utils import VALID_PRIORITIES, VALID_STATUSES


class TaskManager:
    """Manage a collection of Task objects."""

    def __init__(self, tasks=None):
        """Initialize the manager with an optional list of tasks."""
        self.tasks = list(tasks) if tasks else []
        self.next_id = max(
            (task.task_id for task in self.tasks),
            default=0
        ) + 1

    def add_task(
        self,
        title,
        assignee,
        priority="medium",
        due_date=""
    ):
        """Create and add a new task."""
        task = Task(
            task_id=self.next_id,
            title=title,
            assignee=assignee,
            priority=priority,
            due_date=due_date
        )

        self.tasks.append(task)
        self.next_id += 1
        return task

    def find_by_id(self, task_id):
        """Find a task by its unique ID."""
        for task in self.tasks:
            if task.task_id == int(task_id):
                return task

        return None

    def delete_task(self, task_id):
        """Delete a task and return whether it existed."""
        task = self.find_by_id(task_id)

        if task is None:
            return False

        self.tasks.remove(task)
        return True

    def change_status(self, task_id, status):
        """Change a task's status after validating the new status."""
        if status not in VALID_STATUSES:
            return False

        task = self.find_by_id(task_id)

        if task is None:
            return False

        task.status = status
        return True

    def filter_tasks(self, assignee=None, status=None, priority=None):
        """Return tasks matching the supplied filters."""
        filtered = self.tasks

        if assignee:
            filtered = [
                task for task in filtered
                if task.assignee.lower() == assignee.lower()
            ]

        if status:
            filtered = [
                task for task in filtered
                if task.status == status
            ]

        if priority:
            filtered = [
                task for task in filtered
                if task.priority == priority
            ]

        return filtered

    def search(self, keyword):
        """Search task titles and assignee names."""
        keyword = keyword.lower().strip()

        return [
            task for task in self.tasks
            if keyword in task.title.lower()
            or keyword in task.assignee.lower()
        ]

    def overdue_tasks(self):
        """Return all tasks that are overdue."""
        return [task for task in self.tasks if task.is_overdue()]

    def sorted_by_priority(self):
        """Return tasks ordered from high to low priority."""
        priority_order = {
            "high": 1,
            "medium": 2,
            "low": 3
        }

        return sorted(
            self.tasks,
            key=lambda task: priority_order[task.priority]
        )

    def stats(self):
        """Return task statistics in a dictionary."""
        total = len(self.tasks)
        completed = sum(
            1 for task in self.tasks if task.status == "done"
        )
        in_progress = sum(
            1 for task in self.tasks if task.status == "in_progress"
        )
        pending = sum(
            1 for task in self.tasks if task.status == "todo"
        )
        overdue = len(self.overdue_tasks())

        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "overdue": overdue
        }

    def tasks_per_assignee(self):
        """Count how many tasks are assigned to each person."""
        counts = {}

        for task in self.tasks:
            counts[task.assignee] = counts.get(task.assignee, 0) + 1

        return counts
