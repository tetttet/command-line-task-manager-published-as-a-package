## Install

From the project directory, on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

On Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

After activation, run `task` to open the interactive terminal view.
Enter commands at the `❯` prompt, for example `add Write report`, `ls`, or `/help`.
`list` and `ls` are the same command. `list` shows To do tasks, `list --done` shows completed tasks, and `list --all` shows both.
Titles may contain spaces without quotes. `clear` and `cls` clear the interactive screen;
`clear-completed` removes completed tasks. Type `task` at the prompt to show the welcome view again.

Tab completes commands and the arrow keys recall history on terminals with readline.
The welcome screen shows your next task and a small activity chart.

You can also run single commands directly, such as:
`task add "Write report"` or `task --help`. 

To leave the environment, run `deactivate`.

## Commands

| Command | Purpose |
| --- | --- |
| `task add "Write report"` | Add a task |
| `task list` or `task ls` | List To do tasks |
| `task list --done` | List completed tasks |
| `task list --undone` | List To do tasks |
| `task list --all` | List every task |
| `task done 1` | Complete task 1 |
| `task undone 1` | Make task 1 pending |
| `task delete 1` | Delete task 1 |
| `task update 1 "New title"` | Change task 1's title |
| `task show 1` | Show task 1's details |
| `task clear` | Delete completed tasks |
| `task stats` | Show progress and a 7-day completion chart |
| `task demo` | Try 26 sample tasks in a temporary workspace |
| `task help` | Show all commands |

Also available: `task --help`, `task --version`, and `task <command> --help` (for example, `task add --help`). IDs are positive integers. After deletion or a status change, tasks are renumbered from 1, with To do tasks first. Use `list --all` to see current IDs. Existing task files are normalized when read; new IDs are saved on the next change. Titles cannot be blank.

## Try it with sample data

```bash
task demo
```

Or run `python test_task.py` from the project directory. Both open a separate
session with 8 pending and 18 completed tasks spread across the last week.
Try `ls`, `ls --done`, `done 1`, then `stats`. Type `/exit` to leave.
Demo changes are discarded; your own tasks stay untouched.
`task demo --preview` prints the sample list and chart without opening a prompt.

## Progress

`stats` shows task counts, completion percentage, and a daily chart:

```text
Progress  ━━━━━━━━━━━━━━──────  69%

This week · completed tasks

Tue 06  ━━━━              1
Wed 07  ━━━━━━━━━━━━      3
Thu 08  ━━━━━━━━          2
Fri 09  ━━━━━━━━━━━━━━━━  4
Sat 10  ━━━━              1
Sun 11  ━━━━━━━━━━━━      3
Mon 12  ━━━━━━━━━━━━━━━━  4
```

Dates follow your local timezone. `done` records the completion time; `undone`
removes it. The chart counts tasks still in the file, so deleting completed tasks
also removes them from the chart. Older tasks without a completion date still
count toward the total, but not the daily chart.

## Project structure

```text
src/task_manager/
  cli.py            Entry point: one command or interactive mode
  arguments.py      Command names, flags, and ls alias
  commands.py       Add, edit, complete, delete, list
  storage.py        JSON file, validation, task IDs
  productivity.py   Weekly counts and progress
  input.py          Parse commands typed at the prompt
  interactive.py    Input loop and command history
  demo.py           Sample tasks and temporary workspace
  ui/
    theme.py        Colors and terminal sizing
    animation.py    Startup and result transitions
    views.py        Welcome screen, help, and task list
tests/              CLI, interactive, demo, and productivity tests
test_task.py        Start the demo from the project directory
```

A command goes through `cli → arguments → commands → storage`.
Interactive mode adds `input` and `ui`; both modes use the same commands.
No runtime dependencies. Set `TASK_MANAGER_NO_ANIMATION=1` to disable motion,
or `NO_COLOR=1` for plain output. Redirected output has no colors or animation.

## Where tasks are stored

The file is `tasks.json` in `~/Library/Application Support/task-manager/` on macOS, `%APPDATA%\task-manager\` on Windows, or `${XDG_DATA_HOME:-~/.local/share}/task-manager/` on Linux. It is created when a command saves tasks. A missing or empty file means no tasks. If JSON is corrupted, the command reports an error and leaves the file intact.

## Run tests

With the virtual environment active, install pytest separately for development:

```bash
python -m pip install pytest
python -m pytest
```

Tests set `TASK_MANAGER_DATA_DIR` to a temporary directory. Your real task data is never cleared by the test suite.
