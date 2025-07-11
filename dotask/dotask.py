from pathlib import Path
import json
from enum import Enum
from datetime import datetime
from typing import Any, Callable
from dataclasses import dataclass, asdict


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

@dataclass
class Task:
    id: int
    description: str
    status: str
    createdAt: str
    updatedAt: str

class TaskStatus(Enum):
    TODO = "todo"
    DONE = "done"
    IN_PROGRESS = "in-progress"
    


def main(action: Callable, file: str):
    tasks = load_file(file)
    action(tasks)
    if action != list_tasks:
        save_file(file, tasks)

class InvalidTaskFileError(Exception):
    def __init__(self, file: str):
        super().__init__(f"Cannot read tasks from file: {file}")
        self.file = file

def load_file(file: str) -> list[Task]:
    file = Path(file)    
    if not file.exists() or file.stat().st_size == 0:
        return []

    try:
        with open(file, 'r') as task_file:
            return [task for d in json.load(task_file) if (task := dict_to_task(d)) is not None]
    except json.decoder.JSONDecodeError:
        raise(InvalidTaskFileError(str(file)))

        
        
    
def dict_to_task(d: dict) -> Task:
    try:
        return Task(
            id=int(d['id']),
            description=str(d['description']),
            status=d.get('status', 'todo'),
            createdAt=d.get('createdAt', datetime.now().strftime(DATETIME_FORMAT)),
            updatedAt=d.get('updatedAt', datetime.now().strftime(DATETIME_FORMAT)),
        )
    except (KeyError, ValueError) as e:
        print(f"⚠️ Skipping invalid task: {d} ({e})")
        return None    



def save_file(file: str, tasks: list[Task]):
    file = Path(file)
    
    file.parent.mkdir(parents=True, exist_ok=True)

    with open(file, 'w+') as task_file:
        json.dump([asdict(task) for task in tasks], task_file, indent=2, default=str)


def print_task_table(tasks: list[Task]) -> None:
    headers = ["ID", "Description", "Status", "Created At", "Updated At"]
    widths = [5, max(28, max([len(t.description) for t in tasks], default=0)), 12, 20, 20]

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
            task.id,
            task.description,
            task.status,
            task.createdAt,
            task.updatedAt,
        ]
        print(format_row(row))
    print(bottom)


def list_tasks(tasks: list[Task],  status: str, order_by: str) -> None:
    if not (status == 'all'):
        tasks = list(filter(lambda task: task.status == status, tasks))
        
    tasks = sorted(tasks, key=lambda task: getattr(task, order_by))
    print_task_table(tasks)


def add_task(tasks: list[Task], description: str):
    ids = [task.id for task in tasks]

    new_id = 1
    while new_id in ids:
        new_id += 1

    task = Task(
        id=new_id,
        description=description,
        status=TaskStatus.TODO.value,
        createdAt=datetime.now().strftime(DATETIME_FORMAT),
        updatedAt=datetime.now().strftime(DATETIME_FORMAT)
    )

    tasks.append(task)

class TaskNotFoundError(Exception):
    def __init__(self, id: int):
        super().__init__(f"No task found with ID {id}")
        self.id = id


def delete_task(tasks: list[Task], id: int):
    for index, task in enumerate(tasks):
        if task.id == id:
            tasks.pop(index)
            return
    raise TaskNotFoundError(id)



def update_task(tasks: list[Task], id: int, status: TaskStatus):
    for index, task in enumerate(tasks):
        if task.id == id:
            task.status = status.value
            task.updatedAt = datetime.now().strftime(DATETIME_FORMAT)
            return
        
    raise TaskNotFoundError(id)
        

