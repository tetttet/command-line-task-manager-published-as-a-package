import json

import pytest

from task_manager.cli import main


def test_add_list_and_persistence(tmp_path, capsys):
    assert main(["add", "Write report"]) == 0
    saved = json.loads((tmp_path / "tasks.json").read_text(encoding="utf-8"))
    assert saved["tasks"][0]["title"] == "Write report"
    assert saved["tasks"][0]["status"] == "pending"
    assert saved["tasks"][0]["created_at"]
    capsys.readouterr()
    assert main(["list"]) == 0
    assert "1. [pending] Write report" in capsys.readouterr().out


def test_edit_status_show_stats_and_clear(tmp_path, capsys):
    assert main(["add", "First"]) == 0
    assert main(["add", "Second"]) == 0
    assert main(["update", "1", "Updated"]) == 0
    assert main(["done", "1"]) == 0
    assert main(["show", "2"]) == 0
    assert "Title: Updated\nStatus: completed" in capsys.readouterr().out
    assert main(["stats"]) == 0
    assert "Total: 2\nCompleted: 1\nPending: 1" in capsys.readouterr().out
    assert main(["undone", "2"]) == 0
    assert main(["done", "2"]) == 0
    assert main(["clear"]) == 0
    saved = json.loads((tmp_path / "tasks.json").read_text(encoding="utf-8"))
    assert [(task["id"], task["status"]) for task in saved["tasks"]] == [(1, "pending")]


def test_delete_keeps_ids_unique(tmp_path):
    assert main(["add", "First"]) == 0
    assert main(["delete", "1"]) == 0
    assert main(["add", "Second"]) == 0
    saved = json.loads((tmp_path / "tasks.json").read_text(encoding="utf-8"))
    assert [task["id"] for task in saved["tasks"]] == [1]


def test_errors_and_empty_storage(tmp_path, capsys):
    assert main(["list"]) == 0
    assert "No tasks yet" in capsys.readouterr().out
    (tmp_path / "tasks.json").write_text("", encoding="utf-8")
    assert main(["stats"]) == 0
    assert "Total: 0" in capsys.readouterr().out
    assert main(["add", "   "]) == 1
    assert "cannot be empty" in capsys.readouterr().err
    assert main(["show", "1"]) == 1
    assert "not found" in capsys.readouterr().err
    (tmp_path / "tasks.json").write_text("{broken", encoding="utf-8")
    assert main(["add", "Safe"]) == 1
    assert "invalid JSON" in capsys.readouterr().err
    assert (tmp_path / "tasks.json").read_text(encoding="utf-8") == "{broken"


def test_cli_help_and_invalid_id(capsys):
    assert main(["help"]) == 0
    assert "Show all commands" in capsys.readouterr().out
    for args in (["--help"], ["--version"], ["add", "--help"], ["done", "0"]):
        with pytest.raises(SystemExit) as exit_info:
            main(args)
        assert exit_info.value.code == (2 if args == ["done", "0"] else 0)


def test_list_filters_and_ids_follow_visible_pending_tasks(tmp_path, capsys):
    for title in ("First", "Second", "Third"):
        assert main(["add", title]) == 0
    assert main(["done", "1"]) == 0
    capsys.readouterr()
    assert main(["list"]) == 0
    assert capsys.readouterr().out == "1. [pending] Second\n2. [pending] Third\n"
    assert main(["list", "--undone"]) == 0
    assert capsys.readouterr().out == "1. [pending] Second\n2. [pending] Third\n"
    assert main(["list", "--done"]) == 0
    assert capsys.readouterr().out == "3. [completed] First\n"
    assert main(["delete", "1"]) == 0
    capsys.readouterr()
    assert main(["list", "--all"]) == 0
    assert capsys.readouterr().out == "1. [pending] Third\n2. [completed] First\n"
    saved = json.loads((tmp_path / "tasks.json").read_text(encoding="utf-8"))
    assert [task["id"] for task in saved["tasks"]] == [1, 2]
    assert saved["next_id"] == 3


def test_existing_gapped_ids_are_normalized(tmp_path, capsys):
    old_data = {"next_id": 4, "tasks": [
        {"id": 2, "title": "Done", "status": "completed", "created_at": "now"},
        {"id": 3, "title": "To do", "status": "pending", "created_at": "now"},
    ]}
    (tmp_path / "tasks.json").write_text(json.dumps(old_data), encoding="utf-8")
    assert main(["list"]) == 0
    assert capsys.readouterr().out == "1. [pending] To do\n"
    assert main(["list", "--done"]) == 0
    assert capsys.readouterr().out == "2. [completed] Done\n"
    assert main(["delete", "1"]) == 0
    saved = json.loads((tmp_path / "tasks.json").read_text(encoding="utf-8"))
    assert [(task["id"], task["title"]) for task in saved["tasks"]] == [(1, "Done")]


@pytest.mark.parametrize("options", [[], ["--done"], ["--undone"], ["--all"]])
def test_ls_matches_list_with_sample_tasks(sample_tasks, options, capsys):
    assert len(sample_tasks) == 26
    assert main(["list", *options]) == 0
    expected = capsys.readouterr().out
    assert main(["ls", *options]) == 0
    assert capsys.readouterr().out == expected


def test_completion_date_survives_repeated_done_and_resets_on_undone(tmp_path):
    assert main(["add", "Prepare presentation"]) == 0
    assert main(["done", "1"]) == 0
    path = tmp_path / "tasks.json"
    completed_at = json.loads(path.read_text())["tasks"][0]["completed_at"]
    assert main(["done", "1"]) == 0
    assert json.loads(path.read_text())["tasks"][0]["completed_at"] == completed_at
    assert main(["undone", "1"]) == 0
    assert "completed_at" not in json.loads(path.read_text())["tasks"][0]


def test_sample_tasks_keep_consecutive_ids_after_mutations(sample_tasks, tmp_path):
    for args in (["done", "3"], ["delete", "2"], ["undone", "25"], ["add", "Защитить проект"]):
        assert main(args) == 0
    saved = json.loads((tmp_path / "tasks.json").read_text())
    assert [task["id"] for task in saved["tasks"]] == list(range(1, 27))
    assert saved["next_id"] == 27
    statuses = [task["status"] for task in saved["tasks"]]
    assert statuses == sorted(statuses, reverse=True)
