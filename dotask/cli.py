import argparse
from dotask.dotask import *

global_parser = argparse.ArgumentParser(
    prog='test',
    description="A lightweight command-line tool for managing tasks. Add, update, delete, and track tasks.",
)

class VerboseStore(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        mapping = {'todo': TaskStatus.TODO, 'in-progress': TaskStatus.IN_PROGRESS, 'done': TaskStatus.DONE}
        setattr(namespace, self.dest, mapping[value])

global_parser.add_argument('-f', '--file', default='./dotask/tasks.json', help='file path to tasks')

subparsers = global_parser.add_subparsers(title='actions', help='chose what to do with a task list')
subparsers.required = True

add_parser = subparsers.add_parser('add', help='add a new task')
add_parser.add_argument('description')
add_parser.set_defaults(action=add_task)

update_parser = subparsers.add_parser('update', help='update a task')
update_parser.add_argument('id', type=int)
update_parser.add_argument('status', choices=['todo', 'in-progress', 'done'], action=VerboseStore)
update_parser.set_defaults(action=update_task)

delete_parser = subparsers.add_parser('delete', help='delete a task')
delete_parser.add_argument('id', type=int)
delete_parser.set_defaults(action=delete_task)

list_parser = subparsers.add_parser('list', help='list tasks')
list_parser.set_defaults(action=list_tasks)

args = global_parser.parse_args()




