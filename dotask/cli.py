import argparse
from dotask.dotask import *
from dotask.dotask import main as run_main
from functools import partial

DEFAULT_DATA_FILE =  Path.home() / '.dotask' / 'tasks.json'

global_parser = argparse.ArgumentParser(
    prog='test',
    description="A lightweight command-line tool for managing tasks. Add, update, delete, and track tasks.",
)

class VerboseStore(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        mapping = {'todo': TaskStatus.TODO, 'in-progress': TaskStatus.IN_PROGRESS, 'done': TaskStatus.DONE}
        setattr(namespace, self.dest, mapping[value])

global_parser.add_argument('-f', '--file', default=DEFAULT_DATA_FILE, help='file path to tasks')

subparsers = global_parser.add_subparsers(title='actions', help='chose what to do with a task list')
subparsers.required = True

add_parser = subparsers.add_parser('add', help='add a new task')
add_parser.add_argument('description')
add_parser.set_defaults(action=lambda args: partial(add_task, description=args.description))

update_parser = subparsers.add_parser('update', help='update a task')
update_parser.add_argument('id', type=int)
update_parser.add_argument('status', choices=['todo', 'in-progress', 'done'], action=VerboseStore)
update_parser.set_defaults(action=lambda args: partial(update_task, id=args.id, status=args.status))

delete_parser = subparsers.add_parser('delete', help='delete a task')
delete_parser.add_argument('id', type=int)
delete_parser.set_defaults(action=lambda args: partial(delete_task, id=args.id))

list_parser = subparsers.add_parser('list', help='list tasks')
list_parser.add_argument('-s', '--status', choices=['all', 'done', 'todo', 'in-progress'], default='all')
list_parser.add_argument('-o', '--order-by', dest='order_by', choices=['id','status', 'createdAt', 'updatedAt'], default='createdAt')
list_parser.set_defaults(action=lambda args: partial(list_tasks, status=args.status, order_by=args.order_by))



def main():
    args = global_parser.parse_args()

    try:
        # Call dotask.dotask.main with action and file
        run_main(args.action(args), args.file)
    except TaskNotFoundError as e:
        print(f"⚠️  {e}")
        exit(1)
    except InvalidTaskFileError as e:
        print(f"❌  {e}")
        exit(1)







