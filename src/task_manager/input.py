import shlex


def parse_command(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("/"):
        line = line[1:]
    parts = line.split(maxsplit=1)
    if not parts:
        return ["help"]
    command, rest = parts[0], parts[1] if len(parts) > 1 else ""
    command = command.lower()
    command = "list" if command == "ls" else command
    rest = rest.strip()
    if command == "task":
        return parse_command(rest) if rest else ["home"]
    if rest in {"--help", "-h"}:
        return [command, rest]
    if command == "add":
        if rest.startswith(('"', "'")):
            words = shlex.split(rest)
            if len(words) == 1:
                rest = words[0]
        return [command, rest] if rest else [command]
    if command == "update":
        parts = rest.split(maxsplit=1)
        task_id = parts[0] if parts else ""
        title = parts[1].strip() if len(parts) > 1 else ""
        if title.startswith(('"', "'")):
            words = shlex.split(title)
            if len(words) == 1:
                title = words[0]
        return [command, task_id, title] if title else [command, task_id] if task_id else [command]
    return [command, *shlex.split(rest)]


