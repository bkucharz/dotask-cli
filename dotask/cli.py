import argparse
from dotask.dotask import *

global_parser = argparse.ArgumentParser(
    prog='test',
    description="A lightweight command-line tool for managing tasks. Add, update, delete, and track tasks.",
)

global_parser.add_argument('-f', '--file', default='./dotask/tasks.json', help='file path to tasks')

subparsers = global_parser.add_subparsers(title='actions', help='chose what to do with a task list')
subparsers.required = True

add_parser = subparsers.add_parser('add', help='add a new task')
add_parser.add_argument('description')
add_parser.set_defaults(action=add_task)

update_parser = subparsers.add_parser('update', help='update a task')

delete_parser = subparsers.add_parser('delete', help='delete a task')
delete_parser.add_argument('id', type=int)
delete_parser.set_defaults(action=delete_task)

list_parser = subparsers.add_parser('list', help='list tasks')
list_parser.set_defaults(action=list_tasks)

args = global_parser.parse_args()




