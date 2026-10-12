import json

from task_manager.cli import main


def test_interactive_session_accepts_full_titles_and_recovers_from_errors(monkeypatch, tmp_path, capsys):
    entries = iter(["add Write report this week", "unknown", "/done 1", "list", "/exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(entries))
    assert main([]) == 0
    output = capsys.readouterr().out
    assert "Welcome back" in output
    assert "Unknown command: unknown" in output
    assert "Write report this week" in output
    assert "Goodbye" in output
    saved = json.loads((tmp_path / "tasks.json").read_text(encoding="utf-8"))
    assert saved["tasks"][0]["status"] == "completed"


def test_interactive_clear_and_cls_keep_tasks(monkeypatch, tmp_path, capsys):
    entries = iter(["add Keep me", "done 1", "clear", "cls", "list", "/exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(entries))
    assert main([]) == 0
    output = capsys.readouterr().out
    assert output.count("Welcome back") == 3
    assert "Keep me" in output
    saved = json.loads((tmp_path / "tasks.json").read_text(encoding="utf-8"))
    assert len(saved["tasks"]) == 1


def test_interactive_clear_completed_removes_tasks(monkeypatch, tmp_path):
    entries = iter(["add Remove me", "done 1", "clear-completed", "/exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(entries))
    assert main([]) == 0
    saved = json.loads((tmp_path / "tasks.json").read_text(encoding="utf-8"))
    assert saved["tasks"] == []


def test_interactive_task_prefix_and_filtered_list(monkeypatch, capsys):
    entries = iter(["add First", "done 1", "task list", "task list --done", "task", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(entries))
    assert main([]) == 0
    output = capsys.readouterr().out
    assert "No pending tasks." in output
    assert "Completed" in output
    assert "First" in output
    assert "Unknown command: task" not in output
    assert output.count("Welcome back") == 2


def test_interactive_aliases_help_and_invalid_quotes(monkeypatch, capsys):
    entries = iter(["/", "add --help", 'add "unclosed', "add Test aliases", "/ls", "task ls --all", "stats", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(entries))
    assert main([]) == 0
    output = capsys.readouterr().out
    assert "No closing quotation" in output
    assert "task add" in output
    assert "Test aliases" in output
    assert "Your momentum" in output
    assert "Unknown command" not in output


def test_narrow_welcome_fits_terminal(monkeypatch, capsys, sample_tasks):
    import os
    from task_manager.ui.theme import cells
    from task_manager.ui.views import welcome

    monkeypatch.setattr("shutil.get_terminal_size", lambda fallback: os.terminal_size((36, 24)))
    welcome()
    lines = capsys.readouterr().out.splitlines()
    frame = [line for line in lines if line.startswith(("│", "╭", "╰"))]
    assert frame
    assert all(cells(line) <= 34 for line in frame)


def test_no_color_disables_ansi_and_animation(monkeypatch, capsys):
    from task_manager.ui.animation import startup
    from task_manager.ui.theme import ACCENT, animated, paint

    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    assert not animated()
    assert paint("hello", ACCENT) == "hello"
    startup()
    assert capsys.readouterr().out == ""
