"""
CLI — command-line interface for konomi directory operations.

Usage:
    python -m konomi.ops.cli packages
    python -m konomi.ops.cli package isa88
    python -m konomi.ops.cli tags [--package isa88]
    python -m konomi.ops.cli read TAG_PATH
    python -m konomi.ops.cli search PATTERN
    python -m konomi.ops.cli compile [--package isa88] [--output file.l5x]
    python -m konomi.ops.cli summary
"""

import argparse
import json
import sys
from konomi.ops.directory_ops import DirectoryOps


class CLI:
    """Command-line interface wrapping DirectoryOps."""

    def __init__(self):
        self.ops = DirectoryOps()

    def run(self, argv: list[str] = None) -> int:
        parser = argparse.ArgumentParser(
            prog="konomi-ops",
            description="KONOMI — directory operations CLI",
        )
        sub = parser.add_subparsers(dest="command")

        # packages
        sub.add_parser("packages", help="List all subpackages")

        # package <name>
        p_pkg = sub.add_parser("package", help="Show package details")
        p_pkg.add_argument("name")

        # tags
        p_tags = sub.add_parser("tags", help="List tags")
        p_tags.add_argument("--package", "-p", default=None)

        # read
        p_read = sub.add_parser("read", help="Read a tag value")
        p_read.add_argument("path")

        # search
        p_search = sub.add_parser("search", help="Search tags by pattern")
        p_search.add_argument("pattern")

        # compile
        p_compile = sub.add_parser("compile", help="Compile tags to L5X")
        p_compile.add_argument("--package", "-p", default=None)
        p_compile.add_argument("--output", "-o", default=None)
        p_compile.add_argument("--project", default="KONOMI")

        # summary
        sub.add_parser("summary", help="Full system summary")

        args = parser.parse_args(argv)

        if not args.command:
            parser.print_help()
            return 1

        handler = getattr(self, f"_cmd_{args.command}", None)
        if not handler:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1

        result = handler(args)
        if not result.ok:
            print(f"ERROR: {result.error}", file=sys.stderr)
            return 1

        if isinstance(result.data, str):
            print(result.data)
        elif isinstance(result.data, list):
            for item in result.data:
                if isinstance(item, dict):
                    print(f"  {item.get('name', '')}  {item.get('desc', '')}")
                else:
                    print(f"  {item}")
        elif isinstance(result.data, dict):
            print(json.dumps(result.data, indent=2, default=str))
        return 0

    def _cmd_packages(self, args):
        return self.ops.list_packages()

    def _cmd_package(self, args):
        return self.ops.get_package(args.name)

    def _cmd_tags(self, args):
        return self.ops.list_tags(args.package)

    def _cmd_read(self, args):
        return self.ops.read_tag(args.path)

    def _cmd_search(self, args):
        return self.ops.search_tags(args.pattern)

    def _cmd_compile(self, args):
        if args.output:
            return self.ops.export_l5x(args.output, args.package, args.project)
        return self.ops.compile_l5x(args.package, args.project)

    def _cmd_summary(self, args):
        return self.ops.summary()


def main():
    cli = CLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
