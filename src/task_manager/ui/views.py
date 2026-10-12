import re

from .. import __version__
from ..productivity import weekly_counts
from ..storage import StorageError, load_data
from .animation import reveal
from .theme import ACCENT, BOLD, GREEN, MUTED, RED, cells, clean, fit, paint, width


HELP = (
    ("add <title>", "Create a task"),
    ("list / ls", "Show To do tasks"),
    ("ls --done / --all", "Completed / every task"),
    ("done / undone <id>", "Change status"),
    ("update <id> <title>", "Rename a task"),
    ("show <id>", "Task details"),
    ("delete <id>", "Remove a task"),
    ("stats", "Progress and weekly chart"),
    ("demo", "Try a separate sample workspace"),
    ("clear / cls", "Clear the terminal"),
    ("clear-completed", "Remove completed tasks"),
    ("task / home", "Show the welcome view"),
    ("/exit", "Close this session"),
)


def welcome() -> None:
    inner = width() - 2
    label = fit(f" Task Manager · v{__version__} ", inner)
    print()
    print(paint("╭" + label + "─" * (inner - cells(label)) + "╮", ACCENT))

    def padded(text: str, size: int, color: str = "") -> str:
        text = fit(text, size)
        return paint(text, color) + " " * (size - cells(text))

    def row(left: str = "", right: str | None = None, color: str = "") -> None:
        if right is None:
            body = padded(left, inner, color)
        else:
            split = 33
            body = padded(left, split, color) + paint("│", MUTED) + padded(right, inner - split - 2, color) + " "
        print(paint("│", MUTED) + body + paint("│", MUTED))

    try:
        tasks = load_data()["tasks"]
        done = sum(task["status"] == "completed" for task in tasks)
        counts = [count for _, count in weekly_counts(tasks)]
        peak = max(counts) or 1
        spark = "".join("▁▂▃▄▅▆▇█"[round(count / peak * 7)] for count in counts)
        next_task = next((task for task in tasks if task["status"] == "pending"), None)
        next_title = f"#{next_task['id']} {next_task['title']}" if next_task else "All clear. Add your next task."
        summary = f"{len(tasks) - done} to do   /   {done} completed"
        if inner >= 72:
            row("", "")
            row("       Welcome back", "   This week", BOLD)
            row("", "")
            row("            ▗▄▄▄▖", f"   {spark}   {sum(counts)} completed", ACCENT)
            row("            ▐▪ ▪▌", "   Last 7 days · stats for details", MUTED)
            row("            ▝▀▀▀▘", "")
            row("", "   Up next", BOLD)
            row("   " + summary, "   " + next_title)
            row("   Local workspace · Python CLI", "   ls to view your tasks", MUTED)
            row("", "")
        else:
            row()
            row("   ✳  Welcome back", color=BOLD)
            row("   Your tasks, one place.", color=MUTED)
            row()
            row("   " + summary)
            row(f"   {spark}   {sum(counts)} this week", color=GREEN)
            row("   Up next  " + next_title, color=MUTED)
            row()
    except StorageError:
        row("   Welcome back", color=BOLD)
        row("   Tasks unavailable — check your data file", color=RED)
    print(paint("╰" + "─" * inner + "╯", MUTED))
    print("  " + paint(fit("/help commands · stats progress · /exit quit", width() - 2), MUTED))
    print()


def show_help() -> None:
    print("  " + paint("Commands", BOLD))
    for command, hint in HELP:
        if width() < 62:
            print("  " + paint(command, ACCENT))
            print("    " + paint(hint, MUTED))
        else:
            print(f"  {paint(command.ljust(26), ACCENT)}{paint(hint, MUTED)}")
    print("\n  Commands accept a leading / or task prefix.")
    print("  Tab completes commands; ↑ / ↓ recalls history where supported.")
    print("  IDs change after edits. Use ls to see current IDs.")


def show_result(command: str, message: str, is_error: bool, args: list[str] | None = None) -> None:
    if not message:
        return
    lines = []
    if command in {"list", "ls"} and not is_error:
        heading = "Completed" if args and "--done" in args else "All tasks" if args and "--all" in args else "To do"
        lines.append("  " + paint(heading, BOLD))
        count = 0
        for line in message.splitlines():
            match = re.fullmatch(r"(\d+)\. \[(pending|completed)\] (.*)", line)
            if match:
                task_id, status, title = match.groups()
                done = status == "completed"
                symbol = paint("✓", GREEN) if done else paint("○", ACCENT)
                lines.append(f"  {symbol}  {paint(task_id.rjust(3), MUTED)}  {paint(fit(title, width() - 11), MUTED) if done else fit(title, width() - 11)}")
                count += 1
            else:
                lines.append("  " + paint(clean(line), MUTED))
        if count:
            lines += ["", "  " + paint(f"{count} task(s) · done <id> to complete · stats to see progress", MUTED)]
    elif command == "stats" and not is_error:
        lines.append("  " + paint("Your momentum", BOLD))
        for line in message.splitlines():
            color = GREEN if "━" in line else MUTED if line.startswith("Chart") else ""
            lines.append("  " + paint(line, color))
    else:
        marker = paint("✕", RED) if is_error else paint("●", GREEN)
        lines = [f"  {marker if index == 0 else ' '}  {clean(line)}" for index, line in enumerate(message.splitlines())]
    reveal(lines)
