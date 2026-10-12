"""Render real CLI demo output as portable, selectable SVG terminal previews.

Run from the repository root: python3 scripts/render_website_previews.py
No third-party dependencies; personal task data is never used.
"""
import contextlib
from datetime import datetime, timezone
import html
import io
import os
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from task_manager.demo import sample_data
from task_manager.productivity import format_stats, weekly_counts
from task_manager.storage import save_data
from task_manager.ui import views

PALETTE = {"173": "#d79d76", "114": "#a9c98d", "245": "#a2a69b", "203": "#ef8b7d"}
ANSI = re.compile(r"\x1b\[([0-9;]*)m")


def render(name, output):
    lines = output.strip("\n").splitlines()
    font = min(18, 346 / max(len(lines), 1))
    height = font * 1.35
    top = (410 - len(lines) * height) / 2 + font
    elements = ['<svg xmlns="http://www.w3.org/2000/svg" width="940" height="410" viewBox="0 0 940 410">',
                '<rect width="940" height="410" fill="#131613"/>',
                '<g font-family="DejaVu Sans Mono, Menlo, Consolas, monospace" style="white-space:pre" xml:space="preserve">']
    for index, line in enumerate(lines):
        color, weight, offset, spans = "#e7eadf", "normal", 0, []
        for match in ANSI.finditer(line):
            spans.append(f'<tspan fill="{color}" font-weight="{weight}">{html.escape(line[offset:match.start()]).replace(' ', '&#160;')}</tspan>')
            code = match.group(1)
            if code == "0":
                color, weight = "#e7eadf", "normal"
            elif code == "1":
                weight = "bold"
            elif code.startswith("38;5;"):
                color = PALETTE.get(code.split(";")[-1], color)
            offset = match.end()
        spans.append(f'<tspan fill="{color}" font-weight="{weight}">{html.escape(line[offset:]).replace(' ', '&#160;')}</tspan>')
        elements.append(f'<text x="28" y="{top + index * height:.2f}" font-size="{font:.2f}">{"".join(spans)}</text>')
    elements.append('</g></svg>')
    (ROOT / "website" / "assets" / f"{name}.svg").write_text("\n".join(elements), encoding="utf-8")


def capture(callback):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        callback()
    return stream.getvalue()


if __name__ == "__main__":
    now = datetime(2026, 10, 12, 12, tzinfo=timezone.utc)
    data = sample_data(now)
    with TemporaryDirectory(prefix="task-website-") as directory, patch.dict(os.environ, {"TASK_MANAGER_DATA_DIR": directory}), patch("task_manager.ui.theme.styled", return_value=True), patch("task_manager.ui.theme.animated", return_value=False), patch.object(views, "width", return_value=78), patch.object(views, "weekly_counts", side_effect=lambda tasks: weekly_counts(tasks, now.date())):
        save_data(data)
        render("workspace", capture(views.welcome))
        listing = "\n".join(f"{task['id']}. [pending] {task['title']}" for task in data["tasks"] if task["status"] == "pending")
        render("tasks", capture(lambda: views.show_result("list", listing, False)))
        render("progress", capture(lambda: views.show_result("stats", format_stats(data["tasks"], now.date()), False)))
    print("Rendered workspace, task list, and progress previews from isolated demo data.")
