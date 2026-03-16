#!/usr/bin/env python3
"""
runmd — Execute and import Python code blocks from Markdown files.

The .md file IS the program. Documentation and code in one file.
No separate .py needed. Single point of truth.

Usage (run):
    python runmd.py README.md              # run all python blocks
    python runmd.py README.md --block 2    # run only block 2
    python runmd.py README.md --list       # list code blocks
    python runmd.py README.md --extract    # print extracted Python

Usage (import hook — lets Python import .md files as modules):
    import runmd
    runmd.install()  # now 'import mymodule' finds mymodule.md

Blocks are detected by ```python ... ``` fences.
"""

import sys
import re
import os
import types
import importlib
import importlib.abc
import importlib.machinery
import importlib.util

# ── Block extraction ─────────────────────────────────────────────────

_BLOCK_RE = re.compile(r'^```python\s*\n(.*?)^```', re.MULTILINE | re.DOTALL)


def extract_blocks(md_text: str) -> list[dict]:
    """Extract all ```python code blocks from markdown text."""
    blocks = []
    for i, match in enumerate(_BLOCK_RE.finditer(md_text)):
        code = match.group(1)
        line_start = md_text[:match.start()].count('\n') + 1
        blocks.append({
            "index": i,
            "line": line_start,
            "code": code,
            "preview": code.strip().split('\n')[0][:60],
        })
    return blocks


def extract_source(md_text: str) -> str:
    """Extract and concatenate all Python blocks into one source string."""
    blocks = extract_blocks(md_text)
    return "\n\n".join(b["code"] for b in blocks)


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


# ── Import hook — lets Python import .md files as modules ────────────

class MarkdownFinder(importlib.abc.MetaPathFinder):
    """Finds .md files on sys.path when a .py file isn't found."""

    def find_spec(self, fullname, path, target=None):
        parts = fullname.split(".")
        tail = parts[-1]

        # Directories to search
        search_dirs = path if path else sys.path

        for d in search_dirs:
            # Check for package: dir/tail/__init__.md
            pkg_init = os.path.join(d, tail, "__init__.md")
            if os.path.isfile(pkg_init):
                return importlib.machinery.ModuleSpec(
                    fullname,
                    MarkdownLoader(pkg_init),
                    origin=pkg_init,
                    is_package=True,
                    submodule_search_locations=[os.path.join(d, tail)],
                )
            # Check for module: dir/tail.md
            mod_file = os.path.join(d, tail + ".md")
            if os.path.isfile(mod_file):
                return importlib.machinery.ModuleSpec(
                    fullname,
                    MarkdownLoader(mod_file),
                    origin=mod_file,
                )
        return None


class MarkdownLoader(importlib.abc.Loader):
    """Loads a .md file by extracting and executing its Python blocks."""

    def __init__(self, path):
        self.path = path

    def create_module(self, spec):
        return None  # use default module creation

    def exec_module(self, module):
        with open(self.path) as f:
            md_text = f.read()
        source = extract_source(md_text)
        module.__file__ = self.path
        module.__md_source__ = True
        code = compile(source, self.path, "exec")
        exec(code, module.__dict__)


_installed = False


def install():
    """Install the .md import hook. Call once at startup."""
    global _installed
    if not _installed:
        sys.meta_path.append(MarkdownFinder())
        _installed = True


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    import argparse
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

    # Install import hook so .md can import other .md files
    install()

    sys.argv = [args.file] + args.args
    return run_blocks(blocks)


if __name__ == "__main__":
    sys.exit(main() or 0)
