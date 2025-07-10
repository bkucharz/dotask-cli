from dotask import cli
from pathlib import Path
import json
from enum import Enum
from datetime import datetime


class TaskStatus(Enum):
    TODO = "todo"
    DONE = "done"
    INPROGRESS = "in progress"
    



def load_file():
    file = Path(cli.args.file)
    if not file.exists() or file.stat().st_size == 0:
        return []
    
    try:
        with open(file, 'r') as task_file:
            return json.load(task_file)
    except json.decoder.JSONDecodeError:
        cli.global_parser.exit(status=1, message=f"Cannot read data from {str(file)}")
    

def print_task_table(tasks):
    headers = ["ID", "Description", "Status", "Created At", "Updated At"]
    widths = [5, max(28, max([len(t['description']) for t in tasks])), 12, 20, 20]

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


def list_tasks():
    tasks = load_file()

    print_task_table(tasks)


def add_task():
    tasks = load_file()
    ids = [task['id'] for task in tasks]
    
    new_id = 1
    while new_id in ids:
        new_id += 1
    
    task = {
        "id": new_id,
        "description": cli.args.description,
        "status": TaskStatus.TODO.value,
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    tasks.append(task)
    
    file = Path(cli.args.file)

    with open(file, 'w+') as task_file:
        json.dump(tasks, task_file, default=str)
        
        
def delete_task():
    tasks = load_file()
    for index, task in enumerate(tasks):
        if task['id'] == cli.args.id:
            break
    else:
        cli.global_parser.exit(2, f"There is no task with id = {cli.args.id}")
        
    tasks.pop(index)

    file = Path(cli.args.file)

    with open(file, 'w+') as task_file:
        json.dump(tasks, task_file, default=str)
    
    