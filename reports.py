"""Generate and save TaskFlow text reports."""


from datetime import datetime
from pathlib import Path

from storage import EXPORT_DIR, ensure_folders


def build_report_text(tasks,statistics):
    """Build a formatted text report from tasks and statistics."""
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lines = [
        "=" * 65,
        "TASKFLOW - TEAM TASK MANAGEMENT REPORT ".center(65),
        "=" * 65,
        f"Generated: {generated_at}",
        "",
        "TASK STATISTICS",
        "-" * 65,
        f"Total tasks:        {statistics['total']}",
        f"Completed tasks:    {statistics['completed']}",
        f"In progress:        {statistics['in_progress']}",
        f"Pending tasks:      {statistics['pending']}",
        f"Overdue tasks:      {statistics['overdue']}",
        "",
        "TASK DETAILS",
        "-" * 65
        
    ]
    
    if not tasks:
        lines.append("No tasks available.")
    else:
        for task in tasks:
            lines.extend([
                f"Task ID: {task.task_id}",
                f"Title: {task.title}",
                f"Assigned to: {task.assignee}",
                f"Priority: {task.priority}",
                f"Status: {task.status}",
                f"Due date: {task.due_date or 'Not specified'}",
                f"Overdue: {'Yes' if task.is_overdue() else 'No'}",
                "-" * 65
            ])
    
    
    
    
    lines.extend([
        "",
        "END OF REPORT",
        "=" * 65
    ])
    
    return "\n".join(lines)


def save_report(report_text):
    """Save the report to a timestamp next files."""
    ensure_folders()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = EXPORT_DIR / f"taskflow_report_{timestamp}.txt"
    
    
    report_file.write_text(report_text, encoding="utf-8")
    
    
    return report_file        
        