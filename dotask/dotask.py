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
    
    
def list_tasks():
    tasks = load_file()
    
    pad = 15
    print('-' * (pad * 5 + 6))
    print(f"|{'id':^{pad}}|{'description':^{pad}}|{'status':^{pad}}|{'createdAt':^{pad}}|{'updatedAt':^{pad}}|")
    print('-' * (pad * 5 + 6))
    
    for task in tasks:
        print(f"|{task['id']:^{pad}}|{task['description']:^{pad}}|{task['status']:^{pad}}|{task['createdAt']:^{pad}}|{task['updatedAt']:^{pad}}|")

    print('-' * (pad * 5 + 6))
    

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

    
    