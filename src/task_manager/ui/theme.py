import os
import shutil
import sys
import unicodedata

ACCENT = "\x1b[38;5;173m"
GREEN = "\x1b[38;5;114m"
MUTED = "\x1b[38;5;245m"
RED = "\x1b[38;5;203m"
BOLD = "\x1b[1m"
RESET = "\x1b[0m"


def styled() -> bool:
    return sys.stdout.isatty() and os.environ.get("TERM") != "dumb" and "NO_COLOR" not in os.environ


def animated() -> bool:
    return styled() and not os.environ.get("TASK_MANAGER_NO_ANIMATION")


def paint(value: str, color: str) -> str:
    return f"{color}{value}{RESET}" if color and styled() else value


def width() -> int:
    return max(12, min(shutil.get_terminal_size((80, 24)).columns - 2, 96))


def clean(value: str) -> str:
    return "".join(char if not unicodedata.category(char).startswith("C") else " " for char in value)


def cells(value: str) -> int:
    return sum(0 if unicodedata.combining(char) else 2 if unicodedata.east_asian_width(char) in "WF" else 1 for char in value)


def fit(value: str, limit: int) -> str:
    value = clean(value)
    if cells(value) <= limit:
        return value
    result = ""
    for char in value:
        if cells(result + char) > limit - 1:
            break
        result += char
    return result + "…"


def rule() -> None:
    print(paint("─" * width(), MUTED))


def prompt() -> str:
    if styled():
        return f"\001{ACCENT}\002❯\001{RESET}\002 "
    return "❯ "
