# TASKFLOW – Team Task Management System
<!-- markdownlint-disable MD033 -->  
<p align="center">
  <strong>A Simple, Efficient and Reliable Command-Line Task Management System</strong>
</p>

<p align="center">
  Built by <strong>DALITECHX TECHNOLOGIES</strong>
  <br>
  <em>Building What Comes Next.</em>
</p>

<p align="center">
  <a href="https://github.com/vscode254-pixel/TaskFlow">GitHub Repository</a>
</p>

---

## About TaskFlow

**TaskFlow** is a Python-based Team Task Management System designed to help individuals and teams organize, assign, track, and manage tasks efficiently through a command-line interface.

The project demonstrates how Python can be used to develop practical software solutions that address everyday organizational challenges.

With TaskFlow, users can create tasks, assign responsibilities, set priorities and deadlines, monitor progress, generate reports, and manage task records.

TaskFlow is developed as a practical software project by **DALITECHX TECHNOLOGIES**.

Our goal is to build technology solutions that solve real problems and create value.

## Key Features

TaskFlow provides several task management capabilities:

- **Task Creation:** Create and manage tasks with relevant details.
- **Task Assignment:** Assign tasks to specific team members.
- **Priority Management:** Organize tasks according to Low, Medium, and High priority levels.
- **Due Date Tracking:** Set deadlines and monitor upcoming tasks.
- **Status Management:** Track tasks through Pending, In Progress, and Completed statuses.
- **Task Searching:** Search for tasks using relevant information.
- **Task Filtering:** Filter tasks based on status, priority, or assignee.
- **Overdue Tracking:** Identify tasks that have passed their deadlines.
- **Task Statistics:** View useful information about task progress and distribution.
- **CSV Export:** Export task records into CSV format.
- **Data Persistence:** Store task information using JSON files.
- **Backup Support:** Create backups of task data.
- **Activity Logging:** Keep a record of important actions.
- **Report Generation:** Generate task management reports.

## Technology Stack

| Technology | Purpose |
:|---|---|
| Python 3.9+ | Main programming language |
| JSON | Task data storage |
| CSV | Data export and import |
| Datetime | Date and deadline management |
| Unittest | Automated testing |
| Git & GitHub | Version control and project collaboration |

TaskFlow uses Python's standard library and does not require third-party packages.

## Project Structure

```text
TaskFlow/
│
├── milestones/
│   └── day1_prototype.py
│
├── data/
│   └── tasks.json
│
├── exports/
│
├── backups/
│
├── logs/
│
├── reports/
│
├── utils.py
├── models.py
├── manager.py
├── storage.py
├── reports.py
├── main.py
├── test_taskflow.py
│
└── README.md
```

## Getting Started

Follow these instructions to run TaskFlow on your local computer.

### 1. Requirements

Before running the project, make sure you have:

- Python 3.9 or later
- Git installed
- A code editor such as Visual Studio Code

### 2. Clone the Repository

Open your terminal and execute:

```bash
git clone https://github.com/vscode254-pixel/TaskFlow.git
```

### 3. Navigate to the Project Directory

```bash
cd TaskFlow
```

### 4. Run the Application

```bash
python main.py
```

If your system uses `python3`, run:

```bash
python3 main.py
```

The TaskFlow command-line menu should appear in your terminal.

## How to Use TaskFlow

After launching the application, follow the menu instructions to access the available features.

You can:

1. Add new tasks.
2. View all tasks.
3. Search for specific tasks.
4. Assign tasks to team members.
5. Change task priorities.
6. Update task statuses.
7. Filter tasks.
8. View overdue tasks.
9. View task statistics.
10. Import and export CSV records.
11. Create data backups.
12. Generate reports.
13. View activity logs.

The application guides users through the available operations using a menu-driven interface.

## Project Architecture

TaskFlow is organized into separate Python modules to make the application easier to understand, maintain, and extend.

| File | Responsibility |
:| :---| :---|
| `main.py` | Application entry point and menu system |
| `utils.py` | Reusable helper functions and input validation |
| `models.py` | Task class and task-related data |
| `manager.py` | Task management operations |
| `storage.py` | File storage, CSV operations, backups and activity logs |
| `reports.py` | Report generation |
| `test_taskflow.py` | Automated application tests |
| `milestones/day1_prototype.py` | Initial procedural prototype |

## Running Tests

TaskFlow includes automated tests using Python's built-in `unittest` framework.

To run the tests, execute:

```bash
python -m unittest -v
```

Or:

```bash
python3 -m unittest -v
```

These tests help verify important application functionality, including task management, data handling, utility functions, and report generation.

## Learning Objectives

This project provides practical experience in:

- Python programming fundamentals.
- Variables, lists, dictionaries, and loops.
- Conditional statements and functions.
- Object-Oriented Programming (OOP).
- Classes and objects.
- Modular programming.
- File handling.
- JSON and CSV operations.
- Exception handling and input validation.
- Date and time management.
- Software testing.
- Git and GitHub version control.
- Building command-line applications.

## Future Improvements

Possible future improvements include:

- A graphical user interface.
- User authentication and role management.
- A web-based version.
- Database integration.
- Team collaboration features.
- Email and deadline notifications.
- Advanced analytics and dashboards.
- Cloud-based data synchronization.

These are potential future enhancements and are not all part of the current implementation.

---

## About DALITECHX TECHNOLOGIES

<p align="center">
  <strong>DALITECHX TECHNOLOGIES</strong>
  <br>
  <em>Building What Comes Next.</em>
</p>

DALITECHX TECHNOLOGIES is a technology-focused company committed to exploring, developing, and delivering practical technology solutions.

We believe technology should do more than demonstrate what is possible. It should solve real-world problems, improve operations, and create meaningful opportunities.

Our areas of interest include:

- Software Development
- Artificial Intelligence and Automation
- Cybersecurity and Digital Trust
- Cloud Technologies
- Digital Platforms
- Business Technology Solutions

We are focused on building practical solutions, developing technical expertise, and creating technology that makes a difference.

## Work With Us

Have a project idea, business challenge, or technology solution you would like to develop?

We would be glad to hear from you.

**Let's discuss how we can turn your ideas into working solutions.**

- **Email:** [Dalitechxtechnologies@gmail.com]
- **Phone / WhatsApp:** +254 745 460 866
- **GitHub:** [https://github.com/vscode254-pixel/TaskFlow]

For project enquiries, collaborations, and technology partnerships, feel free to reach out.

---

## Contributing

Suggestions, improvements, and constructive feedback are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request.

## License

This project currently does not specify an open-source license. Please contact the repository owner before redistributing or using it under different terms.

---

<p align="center">
  <strong>DALITECHX TECHNOLOGIES</strong>
  <br>
  <em>Building What Comes Next.</em>
  <br><br>
  Think. Build. Innovate. Deliver.
</p>

<p align="center">
  <a href="https://github.com/vscode254-pixel/TaskFlow">Explore TaskFlow on GitHub</a>
</p>

<!-- markdownlint-enable MD033 -->