import dotask.cli
from pathlib import Path
import json



def load_file():
    file = Path(dotask.cli.args.file)
    if not file.exists():
        return []
    
    with open(file, 'r') as task_file:
        return json.load(task_file)
    
    
    
def list_tasks():
    tasks = load_file()
    
    pad = 15
    print('-' * (pad * 5 + 6))
    print(f"|{'id':^{pad}}|{'description':^{pad}}|{'status':^{pad}}|{'createdAt':^{pad}}|{'updatedAt':^{pad}}|")
    print('-' * (pad * 5 + 6))
    
    for task in tasks:
        print(f"|{task['id']:^{pad}}|{task['description']:^{pad}}|{task['status']:^{pad}}|{task['createdAt']:^{pad}}|{task['updatedAt']:^{pad}}|")

    print('-' * (pad * 5 + 6))
    
