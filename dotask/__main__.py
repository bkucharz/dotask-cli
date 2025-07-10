from dotask.cli import args
from dotask.dotask import main

main(args.action(args), args.file)
