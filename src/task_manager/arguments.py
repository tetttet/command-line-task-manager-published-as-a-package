import argparse

from . import __version__


def positive_id(value: str) -> int:
    try:
        task_id = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("task ID must be a positive number") from error
    if task_id < 1:
        raise argparse.ArgumentTypeError("task ID must be a positive number")
    return task_id


def parser_for_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="task", description="Manage your tasks.")
    parser.add_argument("--version", action="version", version=f"task {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    descriptions = {
        "add": "Add a new task",
        "list": "List pending tasks (or filter by status)",
        "done": "Mark a task as completed",
        "undone": "Mark a task as pending",
        "delete": "Delete a task",
        "update": "Change a task title",
        "show": "Show task details",
        "clear": "Delete completed tasks",
        "stats": "Show weekly productivity",
        "demo": "Open a session with sample tasks",
        "help": "Show all commands",
    }
    for name, description in descriptions.items():
        command = commands.add_parser(
            name, aliases=["ls"] if name == "list" else [],
            help=description, description=description,
        )
        command.set_defaults(command=name)
        if name in ("done", "undone", "delete", "update", "show"):
            command.add_argument("id", type=positive_id, help="positive task ID")
        if name in ("add", "update"):
            command.add_argument("title", help="task title")
        if name == "demo":
            command.add_argument("--preview", action="store_true", help="print the demo and exit")
        if name == "list":
            filters = command.add_mutually_exclusive_group()
            filters.add_argument("--done", action="store_true", help="show completed tasks")
            filters.add_argument("--undone", action="store_true", help="show pending tasks")
            filters.add_argument("--all", action="store_true", help="show every task")
    return parser


