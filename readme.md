# Task Tracker CLI

A command-line task tracker application built with Python that allows you to manage your tasks efficiently.

## Features

- Add new tasks
- Update existing tasks
- Delete tasks
- Mark tasks as in-progress or done
- List all tasks or filter by status
- Persistent storage using JSON
- Formatted table output for task listings

## Requirements

- Python 3.x

## Installation

No external dependencies required. The application uses only Python standard library.

## Usage

Run the application using Python:

```bash
python app.py [command] [arguments]
```

### Commands

#### Add a Task
```bash
python app.py add "Task description"
```

#### Update a Task
```bash
python app.py update <task_id> "New description"
```

#### Delete a Task
```bash
python app.py delete <task_id>
```

#### Mark Task as In-Progress
```bash
python app.py mark-in-progress <task_id>
```

#### Mark Task as Done
```bash
python app.py mark-done <task_id>
```

#### List Tasks
```bash
python app.py list
```

List tasks with specific status:
```bash
python app.py list todo
python app.py list in-progress
python app.py list done
```

## Data Storage

Tasks are stored in `tasks.json` in the current working directory. Each task contains:
- `id`: Unique identifier
- `description`: Task description
- `status`: Current status (todo, in-progress, done)
- `createdAt`: ISO format timestamp of creation
- `updatedAt`: ISO format timestamp of last update

## Logging

Application logs are stored in `task-traker.log` with DEBUG level logging enabled for troubleshooting.

## Project Structure

```
task-tracker/
├── app.py              # Main entry point and CLI argument parsing
├── src/
│   ├── task_logic.py   # Core task management functions
│   └── utils.py        # Utility functions and data models
├── tasks.json          # Task storage (auto-created)
└── task-traker.log     # Application logs (auto-created)
```

## License

This project is open source and available for personal and commercial use.
project url is `https://roadmap.sh/projects/task-tracker`
