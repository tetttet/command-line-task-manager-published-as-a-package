import os
from datetime import datetime, timedelta
from tempfile import TemporaryDirectory

from .storage import save_data

PENDING = (
    "Prepare the CLI project presentation",
    "Draw the module diagram for the teacher",
    "Practice explaining JSON storage",
    "Review Python decorators",
    "Finish database homework",
    "Read 15 pages of Clean Code",
    "Plan next week's study sessions",
    "Push the final package to GitHub",
)
COMPLETED = (
    "Set up the virtual environment", "Create the package structure",
    "Build the add command", "Save tasks as JSON", "Handle missing files",
    "Implement list filters", "Validate task IDs", "Add update and delete",
    "Write storage tests", "Test Unicode titles", "Fix empty task names",
    "Add command history", "Design the welcome screen", "Add the ls alias",
    "Build the weekly chart", "Check the README examples", "Run the test suite",
    "Rehearse the project demo",
)


def sample_data(now: datetime | None = None) -> dict:
    now = now or datetime.now().astimezone()
    tasks = []
    for title in PENDING:
        tasks.append({"id": len(tasks) + 1, "title": title, "status": "pending",
                      "created_at": (now - timedelta(days=2)).isoformat(timespec="seconds")})
    titles = iter(COMPLETED)
    for days_ago, count in zip(range(6, -1, -1), (1, 3, 2, 4, 1, 3, 4)):
        completed = now - timedelta(days=days_ago)
        for _ in range(count):
            tasks.append({"id": len(tasks) + 1, "title": next(titles), "status": "completed",
                          "created_at": (completed - timedelta(days=1)).isoformat(timespec="seconds"),
                          "completed_at": completed.isoformat(timespec="seconds")})
    return {"next_id": len(tasks) + 1, "tasks": tasks}


def run_demo(preview: bool = False) -> int:
    from .cli import main
    from .productivity import format_stats
    from .ui.views import show_result, welcome

    previous = os.environ.get("TASK_MANAGER_DATA_DIR")
    with TemporaryDirectory(prefix="task-manager-demo-") as directory:
        os.environ["TASK_MANAGER_DATA_DIR"] = directory
        try:
            data = sample_data()
            save_data(data)
            print("\n  DEMO · 26 sample tasks · changes last only for this session")
            if preview:
                welcome()
                message = "\n".join(f"{task['id']}. [{task['status']}] {task['title']}" for task in data["tasks"])
                show_result("list", message, False, ["list", "--all"])
                print()
                show_result("stats", format_stats(data["tasks"]), False)
                return 0
            print("  Try ls, ls --done, done 1, stats. /exit leaves the demo.")
            return main([])
        finally:
            if previous is None:
                os.environ.pop("TASK_MANAGER_DATA_DIR", None)
            else:
                os.environ["TASK_MANAGER_DATA_DIR"] = previous
