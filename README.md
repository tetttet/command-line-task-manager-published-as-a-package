# Task Manager

A small home for the things you need to get done. Add a task, finish it, and watch your week take shape — right in your terminal.

## Install & go

You'll need **Python 3.10+**. On macOS or Linux, paste this into your terminal:

```bash
mkdir test-my-package
cd test-my-package

python3 -m venv .venv
source .venv/bin/activate

pip install student-task-manager-cli
task --help
```

That's it. Run `task` to open your workspace.

<details>
<summary>On Windows? Use PowerShell.</summary>

```powershell
mkdir test-my-package
cd test-my-package

py -m venv .venv
.venv\Scripts\Activate.ps1

pip install student-task-manager-cli
task --help
```

Run `task` to open your workspace.

</details>

The folder holds your Python environment; your tasks live in your user data directory. In a new terminal, return to this folder and activate `.venv` again. Run `deactivate` when you're finished.

## Make yourself at home

The welcome screen gives you a look at what's next and what you've finished this week. It uses warm accents, soft borders, and a little face to keep you company.

```text
             ▗▄▄▄▖
             ▐▪ ▪▌
             ▝▀▀▀▘

       Your tasks, one place.
```

Start with something small. Inside `task`, type:

```text
❯ add Finish the Python assignment
❯ add Take a proper lunch break
❯ ls
❯ done 1
❯ stats
```

You can write titles with spaces, without quotes. Use **Tab** to complete commands and **↑ / ↓** to revisit earlier ones on terminals with readline support. `/help` shows the commands; `/exit` closes the session.

Prefer a quick command from your shell? That works too:

```bash
task add "Finish the Python assignment"
task ls
task done 1
```

## Take it for a spin

Want to see a busy workspace before adding your own tasks?

```bash
task demo
```

You'll get 8 tasks to do and 18 completed over the last week. Try `ls`, `ls --done`, and `stats`, or finish a task yourself. `/exit` leaves the demo and discards its changes. Your own tasks stay untouched.

For a quick look without an interactive session, run `task demo --preview`.

## The commands you'll reach for

These examples run from your shell. Inside the interactive workspace, leave off the `task` prefix.

| Command | What it does |
| --- | --- |
| `task add "Write report"` | Put something on your list |
| `task ls` | See what's left to do |
| `task ls --done` | See what you've finished |
| `task ls --all` | See everything |
| `task done 1` | Mark a task complete |
| `task undone 1` | Put it back on the to-do list |
| `task update 1 "Send the report"` | Rename a task |
| `task show 1` | Take a closer look at a task |
| `task delete 1` | Remove a task |
| `task stats` | See your progress and weekly chart |
| `task clear` | Remove all completed tasks |
| `task help` | See the full command reference |

`list` and `ls` do the same thing. `--undone` explicitly selects pending tasks, which is also the default. Use `task <command> --help` for individual commands, or `task --version` to check your version.

**Task numbers can change.** Pending tasks come first, and the list is renumbered after deletion or a status change. Check `ls --all` before working with an older task number. IDs start at 1; titles can't be blank.

Inside the interactive workspace, `clear` / `cls` clears the screen. Use `clear-completed` to remove finished tasks, and `task` or `home` to bring back the welcome screen.

## A little momentum

`stats` shows your completed share and the last seven days of activity. A sample week looks like this:

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

Dates follow your local timezone. Marking a task done records its completion time; undoing it removes that time. The chart reflects tasks still saved, so deleting completed tasks removes their activity too. Older tasks without a completion date count toward the total, but won't appear on the daily chart.

## Your tasks stay on your machine

Everything is saved in one `tasks.json` file. There's no account to create and no runtime dependencies to install alongside the package.

| System | Default location |
| --- | --- |
| macOS | `~/Library/Application Support/task-manager/tasks.json` |
| Linux | `~/.local/share/task-manager/tasks.json` (uses `XDG_DATA_HOME` when set) |
| Windows | `%APPDATA%\task-manager\tasks.json` |

Set `TASK_MANAGER_DATA_DIR` to use another folder. The file is created on the first save. A missing or empty file starts an empty list; invalid JSON produces an error and leaves the file intact.

For a quieter terminal, set `TASK_MANAGER_NO_ANIMATION=1` to turn off motion or `NO_COLOR=1` to turn off color. Redirected output already skips both.

## Working on the project

From a local checkout on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m pip install pytest
python -m pytest
```

On Windows, create and activate the environment with the PowerShell commands above, then run the same `python -m pip` and test commands. Tests use a temporary data directory, so your own list stays untouched.

The code lives in `src/task_manager/`:

| Files | Responsibility |
| --- | --- |
| `cli.py`, `arguments.py` | Entry point, commands, and flags |
| `commands.py`, `storage.py` | Task operations and JSON storage |
| `interactive.py`, `input.py` | The prompt, history, and input parsing |
| `productivity.py` | Weekly activity and progress |
| `ui/` | Colors, views, and animations |
| `demo.py` | The temporary sample workspace |

Both interactive and single-command modes use the same task operations. Run `python test_task.py` from the checkout to open the demo while developing.

## Package website

The single-page website lives in [`website/`](website/). To preview it locally:

```bash
python3 -m http.server 4173 --directory website
```

Open http://localhost:4173. For Vercel, import this repository and set **Root Directory** to `website` and **Framework Preset** to `Other`. No build step is needed. See the [website setup guide](website/README.md) for details.
