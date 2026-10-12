import sys
from datetime import datetime, timezone

from .productivity import format_stats
from .storage import StorageError, load_data, save_data


def execute(args) -> int:
    if args.command in ("add", "update"):
        title = args.title.strip()
        if not title:
            print("Error: task title cannot be empty.", file=sys.stderr)
            return 1

    try:
        data = load_data()
        tasks = data["tasks"]

        if args.command == "add":
            task = {
                "id": data["next_id"],
                "title": title,
                "status": "pending",
                "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
            tasks.append(task)
            save_data(data)
            print(f"Added task {task['id']}: {title}")
        elif args.command == "list":
            visible = [task for task in tasks if args.all or task["status"] == ("completed" if args.done else "pending")]
            if not visible:
                print("No tasks yet." if not tasks else "No completed tasks." if args.done else "No pending tasks.")
            for task in visible:
                print(f"{task['id']}. [{task['status']}] {task['title']}")
        elif args.command == "stats":
            print(format_stats(tasks))
        elif args.command == "clear":
            remaining = [task for task in tasks if task["status"] != "completed"]
            removed = len(tasks) - len(remaining)
            data["tasks"] = remaining
            save_data(data)
            print(f"Removed {removed} completed task(s).")
        else:
            task = next((task for task in tasks if task["id"] == args.id), None)
            if task is None:
                print(f"Error: task {args.id} not found.", file=sys.stderr)
                return 1
            if args.command == "show":
                print(f"ID: {task['id']}\nTitle: {task['title']}\nStatus: {task['status']}\nCreated: {task['created_at']}")
                if task.get("completed_at"):
                    print(f"Completed: {task['completed_at']}")
            elif args.command == "delete":
                tasks.remove(task)
                save_data(data)
                print(f"Deleted task {args.id}.")
            else:
                if args.command == "update":
                    task["title"] = title
                else:
                    if args.command == "done" and task["status"] != "completed":
                        task["completed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
                    elif args.command == "undone":
                        task.pop("completed_at", None)
                    task["status"] = "completed" if args.command == "done" else "pending"
                save_data(data)
                if args.command == "done":
                    print(f"Completed: {task['title']}")
                elif args.command == "undone":
                    print(f"Back to To do: {task['title']}")
                else:
                    print(f"Renamed task {task['id']}: {task['title']}")
    except StorageError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0
