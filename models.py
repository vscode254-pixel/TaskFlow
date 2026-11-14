
"""Task model and task-related operations."""

from datetime import datetime
from utils import days_until, DATE_FORMAT, VALID_PRIORITIES, VALID_STATUSES


class Task:
    """Represent an individual team task."""

    def __init__(
        self,
        task_id,
        title,
        assignee,
        priority="medium",
        due_date="",
        status="todo",
        created_at=None
    ):
        self.task_id = int(task_id)
        self.title = title.strip()
        self.assignee = assignee.strip()
        self.priority = priority.lower()
        self.due_date = due_date
        self.status = status.lower()
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")

        if not self.title:
            raise ValueError("Task title cannot be empty.")

        if not self.assignee:
            raise ValueError("Assignee cannot be empty.")

        if self.priority not in VALID_PRIORITIES:
            raise ValueError("Invalid task priority.")

        if self.status not in VALID_STATUSES:
            raise ValueError("Invalid task status.")

        if self.due_date:
            if days_until(self.due_date) is None:
                raise ValueError("Invalid due date.")

    def start(self):
        """Mark the task as in progress."""
        if self.status != "done":
            self.status = "in_progress"

    def complete(self):
        """Mark the task as completed."""
        self.status = "done"

    def is_overdue(self):
        """Return True if the task is unfinished and past its due date."""
        remaining_days = days_until(self.due_date)

        return (
            remaining_days is not None
            and remaining_days < 0
            and self.status != "done"
        )

    def to_dict(self):
        """Convert the task into a dictionary for file storage."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "assignee": self.assignee,
            "priority": self.priority,
            "due_date": self.due_date,
            "status": self.status,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task object from a dictionary."""
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            assignee=data["assignee"],
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date", ""),
            status=data.get("status", "todo"),
            created_at=data.get("created_at")
        )

    def __str__(self):
        """Return a readable one-line task description."""
        due = self.due_date if self.due_date else "No due date"

        return (
            f"#{self.task_id} | {self.title} | "
            f"{self.assignee} | {self.priority} | "
            f"{self.status} | Due: {due}"
        )
