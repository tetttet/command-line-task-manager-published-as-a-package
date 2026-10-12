import sys

from .arguments import parser_for_cli
from .commands import execute


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        from .interactive import run_interactive

        return run_interactive(main)
    parser = parser_for_cli()
    args = parser.parse_args(argv)
    if args.command == "help":
        parser.print_help()
        return 0
    if args.command == "demo":
        from .demo import run_demo

        return run_demo(preview=args.preview)
    return execute(args)
