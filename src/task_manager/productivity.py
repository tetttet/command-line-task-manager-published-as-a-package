from datetime import date, datetime, timedelta


def weekly_counts(tasks: list[dict], today: date | None = None) -> list[tuple[date, int]]:
    today = today or datetime.now().astimezone().date()
    counts = {today - timedelta(days=offset): 0 for offset in range(6, -1, -1)}
    for task in tasks:
        if task["status"] != "completed" or not task.get("completed_at"):
            continue
        try:
            completed = datetime.fromisoformat(task["completed_at"]).astimezone().date()
        except (ValueError, TypeError):
            continue
        if completed in counts:
            counts[completed] += 1
    return list(counts.items())


def format_stats(tasks: list[dict], today: date | None = None) -> str:
    completed = sum(task["status"] == "completed" for task in tasks)
    total = len(tasks)
    percent = round(100 * completed / total) if total else 0
    filled = round(20 * completed / total) if total else 0
    lines = [f"Total: {total}", f"Completed: {completed}", f"Pending: {total - completed}", "",
             f"Progress  {'━' * filled}{'─' * (20 - filled)}  {percent}%", "",
             "This week · completed tasks", ""]
    week = weekly_counts(tasks, today)
    peak = max(count for _, count in week) or 1
    for day, count in week:
        bar = '━' * max(1, round(count / peak * 16)) if count else '·'
        lines.append(f"{day:%a %d}  {bar:<16}  {count}")
    lines += ["", f"{sum(count for _, count in week)} completed in the last 7 days"]
    undated = sum(task["status"] == "completed" and not task.get("completed_at") for task in tasks)
    if undated:
        lines.append(f"{undated} older completed task(s) without a date")
    lines.append("Chart uses completion dates of tasks still in your list.")
    return "\n".join(lines)
