#!/usr/bin/env python3
"""
runmd — Execute Python code blocks from Markdown files.

The .md file IS the program. Documentation and code in one file.
No separate .py needed. Single point of truth.

Usage:
    python runmd.py README.md              # run all python blocks
    python runmd.py README.md --block 2    # run only block 2
    python runmd.py README.md --list       # list code blocks
    python runmd.py README.md --extract    # print extracted Python

Blocks are detected by ```python ... ``` fences.
"""

import sys
import re
import argparse


def extract_blocks(md_text: str) -> list[dict]:
    """Extract all ```python code blocks from markdown text."""
    pattern = re.compile(
        r'^```python\s*\n(.*?)^```',
        re.MULTILINE | re.DOTALL,
    )
    blocks = []
    for i, match in enumerate(pattern.finditer(md_text)):
        code = match.group(1)
        line_start = md_text[:match.start()].count('\n') + 1
        blocks.append({
            "index": i,
            "line": line_start,
            "code": code,
            "preview": code.strip().split('\n')[0][:60],
        })
    return blocks


def run_blocks(blocks: list[dict], namespace: dict = None):
    """Execute code blocks in sequence, sharing namespace."""
    ns = namespace or {"__name__": "__main__"}
    for block in blocks:
        try:
            exec(compile(block["code"], f"<md-block-{block['index']}>",
                         "exec"), ns)
        except SystemExit:
            raise
        except Exception as e:
            print(f"[runmd] Error in block {block['index']} "
                  f"(line {block['line']}): {e}", file=sys.stderr)
            return 1
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="runmd — execute Python from Markdown")
    parser.add_argument("file", help="Markdown file to run")
    parser.add_argument("--block", "-b", type=int, default=None,
                        help="Run only this block number")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List code blocks without running")
    parser.add_argument("--extract", "-e", action="store_true",
                        help="Print extracted Python code")
    parser.add_argument("args", nargs="*",
                        help="Arguments passed to the script")

    args = parser.parse_args()

    try:
        with open(args.file) as f:
            md = f.read()
    except FileNotFoundError:
        print(f"[runmd] File not found: {args.file}", file=sys.stderr)
        return 1

    blocks = extract_blocks(md)

    if not blocks:
        print(f"[runmd] No ```python blocks found in {args.file}")
        return 1

    if args.list:
        print(f"[runmd] {len(blocks)} Python blocks in {args.file}:")
        for b in blocks:
            print(f"  Block {b['index']} (line {b['line']}): "
                  f"{b['preview']}")
        return 0

    if args.extract:
        for b in blocks:
            print(f"# --- Block {b['index']} (line {b['line']}) ---")
            print(b["code"])
        return 0

    if args.block is not None:
        blocks = [b for b in blocks if b["index"] == args.block]
        if not blocks:
            print(f"[runmd] Block {args.block} not found")
            return 1

    # Inject sys.argv for the script
    sys.argv = [args.file] + args.args
    return run_blocks(blocks)


if __name__ == "__main__":
    sys.exit(main() or 0)
