import json
import os
import sys
from pathlib import Path


class StorageError(Exception):
    pass


def normalize_data(data: dict) -> None:
    """Pending tasks first, IDs from one."""
    tasks = data["tasks"]
    tasks[:] = ([task for task in tasks if task["status"] == "pending"]
                + [task for task in tasks if task["status"] == "completed"])
    for task_id, task in enumerate(tasks, start=1):
        task["id"] = task_id
    data["next_id"] = len(tasks) + 1


def data_file() -> Path:
    override = os.environ.get("TASK_MANAGER_DATA_DIR")
    if override:
        directory = Path(override)
    elif sys.platform == "win32":
        directory = Path(os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))) / "task-manager"
    elif sys.platform == "darwin":
        directory = Path.home() / "Library" / "Application Support" / "task-manager"
    else:
        directory = Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))) / "task-manager"
    return directory / "tasks.json"


def load_data() -> dict:
    path = data_file()
    try:
        if not path.exists() or path.stat().st_size == 0:
            return {"next_id": 1, "tasks": []}
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, UnicodeError) as error:
        raise StorageError(f"Cannot read task file {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise StorageError(f"Task file {path} contains invalid JSON: {error.msg}") from error

    if (not isinstance(data, dict)
            or type(data.get("next_id")) is not int
            or data["next_id"] < 1
            or not isinstance(data.get("tasks"), list)):
        raise StorageError(f"Task file {path} has an invalid format.")
    ids = set()
    for task in data["tasks"]:
        if (not isinstance(task, dict)
                or type(task.get("id")) is not int
                or task["id"] < 1
                or task["id"] in ids
                or not isinstance(task.get("title"), str)
                or not task["title"].strip()
                or task.get("status") not in ("pending", "completed")
                or not isinstance(task.get("created_at"), str)):
            raise StorageError(f"Task file {path} has an invalid format.")
        ids.add(task["id"])
    if ids and data["next_id"] <= max(ids):
        raise StorageError(f"Task file {path} has an invalid format.")
    normalize_data(data)
    return data


def save_data(data: dict) -> None:
    normalize_data(data)
    path = data_file()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")
    except OSError as error:
        raise StorageError(f"Cannot save task file {path}: {error}") from error
