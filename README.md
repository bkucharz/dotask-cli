# Dotask CLI - A Simple Task Manager

![CLI Task Manager](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

<a href="https://roadmap.sh/projects/task-tracker" target="_blank">
<p align="center">
  <img src="demo.gif" alt="Demo of dotask CLI">
</p>
</a>


Dotask is a lightweight command-line task manager that helps you organize your to-dos efficiently. With a simple interface and powerful features, you can track what you need to do, what you're working on, and what you've completed.

## Features ✨

- ✅ Add, update, and delete tasks
- 📝 Mark tasks as `todo`, `in-progress`, or `done`
- 🔍 Filter tasks by status
- 🗂️ Automatic JSON storage in `~/.dotask/tasks.json`
- 🎨 Beautiful table formatting for task lists
- 🛠️ Configurable task file location

## Installation ⚙️

### Using pip

```bash
pip install git+https://github.com/bkucharz/dotask-cli.git
```

### From source

1. Clone the repository:
   ```bash
   git clone https://github.com/bkucharz/dotask-cli.git
   cd dotask-cli
   ```

2. Install with pip:
   ```bash
   pip install .
   ```

## Usage 🚀

### Basic Commands

```bash
# Add a new task
dotask add "Write documentation"

# List all tasks
dotask list

# Update task status
dotask update 1 done

# Delete a task
dotask delete 1
```

### Advanced Options

```bash
# List only tasks with specific status
dotask list --status done
dotask list --status in-progress
dotask list --status todo

# Sort tasks by different fields
dotask list --order-by id
dotask list --order-by status
dotask list --order-by createdAt
dotask list --order-by updatedAt

# Use a custom task file location
dotask --file /path/to/tasks.json list
```

## Examples 📋

### Adding and Listing Tasks

```bash
$ dotask add "Buy groceries"
$ dotask add "Write unit tests"
$ dotask list
```

Output:
```
┌───────┬──────────────────────────────┬──────────────┬──────────────────────┬──────────────────────┐
│ ID    │ Description                  │ Status       │ Created At           │ Updated At           │
├───────┼──────────────────────────────┼──────────────┼──────────────────────┼──────────────────────┤
│ 1     │ Buy groceries                │ todo         │ 2025-07-11 18:35:23  │ 2025-07-11 18:35:23  │
│ 2     │ Write unit tests             │ todo         │ 2025-07-11 18:35:31  │ 2025-07-11 18:35:31  │
└───────┴──────────────────────────────┴──────────────┴──────────────────────┴──────────────────────┘
```

### Updating Task Status

```bash
$ dotask update 1 in-progress
$ dotask list --status in-progress
```

Output:
```
┌───────┬──────────────────────────────┬──────────────┬──────────────────────┬──────────────────────┐
│ ID    │ Description                  │ Status       │ Created At           │ Updated At           │
├───────┼──────────────────────────────┼──────────────┼──────────────────────┼──────────────────────┤
│ 1     │ Buy groceries                │ in-progress  │ 2025-07-11 18:35:23  │ 2025-07-11 18:36:14  │
└───────┴──────────────────────────────┴──────────────┴──────────────────────┴──────────────────────┘
```

## Configuration ⚙️

By default, tasks are stored in `~/.dotask/tasks.json`. You can specify a different location using the `-f` or `--file` option:

```bash
dotask --file /custom/path/tasks.json add "Custom location task"
```