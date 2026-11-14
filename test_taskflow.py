
"""Automated tests for the TaskFlow application."""

import unittest
import tempfile
from pathlib import Path

from models import Task
from manager import TaskManager
from utils import is_valid_date, days_until
from storage import save_tasks, load_tasks
from reports import build_report_text


class TestTaskModel(unittest.TestCase):
    """Test the Task class."""

    def test_task_creation(self):
        """Test that a task is created with correct details."""
        task = Task(1, "Build website", "Dalton")

        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "Build website")
        self.assertEqual(task.assignee, "Dalton")
        self.assertEqual(task.priority, "medium")
        self.assertEqual(task.status, "todo")

    def test_empty_title_is_rejected(self):
        """Test that an empty title raises an error."""
        with self.assertRaises(ValueError):
            Task(1, "", "Dalton")

    def test_invalid_priority_is_rejected(self):
        """Test that an unsupported priority raises an error."""
        with self.assertRaises(ValueError):
            Task(1, "Build website", "Dalton", priority="urgent")

    def test_complete_task(self):
        """Test marking a task as completed."""
        task = Task(1, "Build website", "Dalton")
        task.complete()

        self.assertEqual(task.status, "done")

    def test_start_task(self):
        """Test marking a task as in progress."""
        task = Task(1, "Build website", "Dalton")
        task.start()

        self.assertEqual(task.status, "in_progress")

    def test_completed_task_does_not_restart(self):
        """Test that starting a completed task does not change its status."""
        task = Task(1, "Build website", "Dalton")
        task.complete()
        task.start()

        self.assertEqual(task.status, "done")

    def test_dictionary_conversion(self):
        """Test converting a task to and from a dictionary."""
        original = Task(1, "Build website", "Dalton", priority="high")

        restored = Task.from_dict(original.to_dict())

        self.assertEqual(restored.task_id, original.task_id)
        self.assertEqual(restored.title, original.title)
        self.assertEqual(restored.priority, original.priority)


class TestTaskManager(unittest.TestCase):
    """Test the TaskManager class."""

    def setUp(self):
        """Create a fresh manager before each test."""
        self.manager = TaskManager()

        self.manager.add_task(
            "Build website",
            "Dalton",
            "high"
        )

        self.manager.add_task(
            "Write documentation",
            "Halima",
            "medium"
        )

    def test_add_task(self):
        """Test adding a task."""
        task = self.manager.add_task(
            "Test application",
            "Kevin"
        )

        self.assertEqual(task.task_id, 3)
        self.assertEqual(len(self.manager.tasks), 3)

    def test_find_task(self):
        """Test finding a task using its ID."""
        task = self.manager.find_by_id(1)

        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Build website")

    def test_find_missing_task(self):
        """Test that a missing task returns None."""
        task = self.manager.find_by_id(99)

        self.assertIsNone(task)

    def test_delete_task(self):
        """Test deleting an existing task."""
        result = self.manager.delete_task(1)

        self.assertTrue(result)
        self.assertEqual(len(self.manager.tasks), 1)

    def test_delete_missing_task(self):
        """Test deleting a task that does not exist."""
        result = self.manager.delete_task(99)

        self.assertFalse(result)

    def test_change_status(self):
        """Test changing the status of a task."""
        result = self.manager.change_status(1, "done")

        self.assertTrue(result)
        self.assertEqual(
            self.manager.find_by_id(1).status,
            "done"
        )

    def test_invalid_status(self):
        """Test rejecting an invalid status."""
        result = self.manager.change_status(1, "finished")

        self.assertFalse(result)

    def test_filter_by_assignee(self):
        """Test filtering tasks by assigned person."""
        results = self.manager.filter_tasks(assignee="Dalton")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].assignee, "Dalton")

    def test_filter_by_status(self):
        """Test filtering tasks by status."""
        self.manager.change_status(1, "done")

        results = self.manager.filter_tasks(status="done")

        self.assertEqual(len(results), 1)

    def test_search(self):
        """Test searching task titles."""
        results = self.manager.search("website")

        self.assertEqual(len(results), 1)

    def test_priority_sorting(self):
        """Test that high-priority tasks appear first."""
        results = self.manager.sorted_by_priority()

        self.assertEqual(results[0].priority, "high")

    def test_statistics(self):
        """Test the task statistics."""
        self.manager.change_status(1, "done")

        statistics = self.manager.stats()

        self.assertEqual(statistics["total"], 2)
        self.assertEqual(statistics["completed"], 1)
        self.assertEqual(statistics["pending"], 1)

    def test_tasks_per_assignee(self):
        """Test counting tasks assigned to each person."""
        counts = self.manager.tasks_per_assignee()

        self.assertEqual(counts["Dalton"], 1)
        self.assertEqual(counts["Halima"], 1)


class TestUtilities(unittest.TestCase):
    """Test reusable validation functions."""

    def test_valid_date(self):
        """Test accepting a correctly formatted date."""
        self.assertTrue(is_valid_date("2026-12-25"))

    def test_invalid_date(self):
        """Test rejecting an incorrectly formatted date."""
        self.assertFalse(is_valid_date("25-12-2026"))

    def test_impossible_date(self):
        """Test rejecting a date that does not exist."""
        self.assertFalse(is_valid_date("2026-02-30"))

    def test_days_until_invalid_date(self):
        """Test that an invalid date returns None."""
        self.assertIsNone(days_until("not-a-date"))


class TestStorageAndReports(unittest.TestCase):
    """Test saving, loading, and generating reports."""

    def test_save_and_load_tasks(self):
        """Test saving and restoring tasks using a temporary file."""
        task = Task(1, "Test storage", "Dalton")

        with tempfile.TemporaryDirectory() as temporary_folder:
            test_file = Path(temporary_folder) / "tasks.json"

            original_save_path = None

            import storage
            original_save_path = storage.TASKS_FILE

            try:
                storage.TASKS_FILE = test_file

                save_tasks([task])
                loaded = load_tasks()

                self.assertEqual(len(loaded), 1)
                self.assertEqual(loaded[0].title, "Test storage")

            finally:
                storage.TASKS_FILE = original_save_path

    def test_report_contains_task_title(self):
        """Test that generated reports contain task details."""
        task = Task(1, "Prepare project report", "Dalton")

        manager = TaskManager([task])

        report = build_report_text(
            manager.tasks,
            manager.stats()
        )

        self.assertIn("Prepare project report", report)
        self.assertIn("TASK STATISTICS", report)


if __name__ == "__main__":
    unittest.main()
