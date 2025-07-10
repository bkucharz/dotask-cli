from pathlib import Path
import json
from enum import Enum
from datetime import datetime
from typing import Any, Callable

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class TaskStatus(Enum):
    TODO = "todo"
    DONE = "done"
    IN_PROGRESS = "in-progress"
    


def main(action: Callable, file: str):
    tasks = load_file(file)
    action(tasks)
    if action != list_tasks:
        save_file(file, tasks)


def load_file(file: str) -> list[dict[str, Any]]:
    file = Path(file)
    if not file.exists() or file.stat().st_size == 0:
        return []

    try:
        with open(file, 'r') as task_file:
            return json.load(task_file)
    except json.decoder.JSONDecodeError:
        print(f"Cannot read data from {str(file)}")
        exit(1)


def save_file(file: str, tasks: list[dict[str, Any]]):
    file = Path(file)

    with open(file, 'w+') as task_file:
        json.dump(tasks, task_file, default=str)


def print_task_table(tasks: list[dict[str, Any]]) -> None:
    headers = ["ID", "Description", "Status", "Created At", "Updated At"]
    widths = [5, max(28, max([len(t['description']) for t in tasks], default=0)), 12, 20, 20]

    def format_row(row):
        return "│ " + " │ ".join(str(cell).ljust(width) for cell, width in zip(row, widths)) + " │"

    top = "┌" + "┬".join("─" * (w + 2) for w in widths) + "┐"
    sep = "├" + "┼".join("─" * (w + 2) for w in widths) + "┤"
    bottom = "└" + "┴".join("─" * (w + 2) for w in widths) + "┘"

    print(top)
    print(format_row(headers))
    print(sep)
    for task in tasks:
        row = [
            task["id"],
            task["description"],
            task["status"],
            task["createdAt"],
            task["updatedAt"],
        ]
        print(format_row(row))
    print(bottom)


def list_tasks(tasks: list[dict[str, Any]],  status: str, order_by: str) -> None:
    if not (status == 'all'):
        tasks = list(filter(lambda task: task['status'] == status, tasks))
        
    tasks = sorted(tasks, key=lambda task: task[order_by])
    print_task_table(tasks)


def add_task(tasks: list[dict[str, Any]], description: str):
    ids = [task['id'] for task in tasks]

    new_id = 1
    while new_id in ids:
        new_id += 1

    task = {
        "id": new_id,
        "description": description,
        "status": TaskStatus.TODO.value,
        "createdAt": datetime.now().strftime(DATETIME_FORMAT),
        "updatedAt": datetime.now().strftime(DATETIME_FORMAT)
    }

    tasks.append(task)


def delete_task(tasks: list[dict[str, Any]], id: int):
    for index, task in enumerate(tasks):
        if task['id'] == id:
            break
    else:
        print(f"There is no task with id = {id}\n")
        exit(1)

    tasks.pop(index)


def update_task(tasks: list[dict[str, Any]], id: int, status: TaskStatus):
    for index, task in enumerate(tasks):
        if task['id'] == id:
            break
    else:
        print(f"There is no task with id = {id}\n")
        exit(1)
        
    task['status'] = status.value
    task['updatedAt'] = datetime.now().strftime(DATETIME_FORMAT)

