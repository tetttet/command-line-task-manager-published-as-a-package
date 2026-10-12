import os

import pytest

from task_manager.cli import main
from task_manager.demo import run_demo


def test_preview_does_not_touch_existing_data(tmp_path, capsys):
    main(["add", "My actual task"])
    path = tmp_path / "tasks.json"
    original = path.read_bytes()
    assert main(["demo", "--preview"]) == 0
    output = capsys.readouterr().out
    assert "26 sample tasks" in output
    assert "Prepare the CLI project presentation" in output
    assert "69%" in output
    assert path.read_bytes() == original
    assert os.environ["TASK_MANAGER_DATA_DIR"] == str(tmp_path)


def test_interactive_demo_keeps_real_tasks(tmp_path, monkeypatch, capsys):
    main(["add", "Keep my homework"])
    original = (tmp_path / "tasks.json").read_bytes()
    entries = iter(["ls", "done 1", "stats", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(entries))
    assert run_demo() == 0
    output = capsys.readouterr().out
    assert "Completed: Prepare the CLI project presentation" in output
    assert "Completed: 19" in output
    assert (tmp_path / "tasks.json").read_bytes() == original


def test_demo_restores_environment_on_failure(monkeypatch):
    monkeypatch.delenv("TASK_MANAGER_DATA_DIR")

    def fail(data):
        raise RuntimeError("write failed")

    monkeypatch.setattr("task_manager.demo.save_data", fail)
    with pytest.raises(RuntimeError, match="write failed"):
        run_demo(preview=True)
    assert "TASK_MANAGER_DATA_DIR" not in os.environ
