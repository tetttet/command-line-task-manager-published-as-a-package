import contextlib
import io
import sys
from collections.abc import Callable

from .input import parse_command
from .ui.animation import startup
from .ui.theme import MUTED, paint, prompt, rule, styled
from .ui.views import show_help, show_result, welcome

COMMANDS = {"add", "list", "ls", "done", "undone", "delete", "update", "show",
            "clear-completed", "stats", "demo"}


@contextlib.contextmanager
def completion():
    try:
        import readline
    except ImportError:
        yield
        return
    previous = readline.get_completer()
    words = sorted(COMMANDS | {"help", "exit", "clear", "cls", "task", "home"})

    def complete(text: str, state: int) -> str | None:
        prefix = "/" if text.startswith("/") else ""
        matches = [prefix + word + " " for word in words if word.startswith(text.lstrip("/"))]
        return matches[state] if state < len(matches) else None

    delimiters = readline.get_completer_delims()
    readline.set_completer_delims(" \t\n")
    readline.set_completer(complete)
    binding = "bind ^I rl_complete" if "libedit" in (readline.__doc__ or "") else "tab: complete"
    readline.parse_and_bind(binding)
    try:
        yield
    finally:
        readline.set_completer(previous)
        readline.set_completer_delims(delimiters)


def run_interactive(execute: Callable[[list[str]], int]) -> int:
    try:
        with completion():
            startup()
            welcome()
            return command_loop(execute)
    except (EOFError, KeyboardInterrupt):
        print("\n  Goodbye.")
        return 0


def command_loop(execute: Callable[[list[str]], int]) -> int:
    while True:
        if styled():
            print(paint("  /help for commands · Tab to complete", MUTED))
            rule()
        line = input(prompt())
        if not line.strip():
            continue
        if styled():
            rule()
        try:
            args = parse_command(line)
        except ValueError as error:
            show_result("", str(error), True)
            continue
        command = args[0]
        if command in {"exit", "quit"}:
            print("  Goodbye.")
            return 0
        if command == "home":
            welcome()
            continue
        if command in {"clear", "cls", "clear-screen"}:
            print("\x1b[2J\x1b[H" if styled() else "", end="")
            welcome()
            continue
        if command == "help":
            show_help()
        elif command not in COMMANDS:
            show_result(command, f"Unknown command: {command}. Type /help for commands.", True)
        elif command == "demo":
            try:
                execute(args)
            except SystemExit:
                pass
            welcome()
        else:
            output, errors = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                try:
                    result = execute(["clear", *args[1:]] if command == "clear-completed" else args)
                except SystemExit as error:
                    result = error.code
            show_result(command, (errors if result else output).getvalue().strip(), bool(result), args)
        print()
