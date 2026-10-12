import sys
import time

from .theme import ACCENT, animated, paint


def startup() -> None:
    if not animated():
        return
    try:
        sys.stdout.write("\x1b[?25l")
        for frame in ("·", "✢", "✳", "✶", "✳", "✢"):
            sys.stdout.write("\r  " + paint(frame + "  Opening your workspace", ACCENT))
            sys.stdout.flush()
            time.sleep(0.055)
    finally:
        sys.stdout.write("\r\x1b[2K\x1b[?25h")
        sys.stdout.flush()


def reveal(lines: list[str]) -> None:
    motion = animated()
    for index, line in enumerate(lines):
        print(line, flush=motion)
        if motion and index < 10:
            time.sleep(0.012)
