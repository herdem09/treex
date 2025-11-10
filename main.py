#!/usr/bin/env python3
"""
TreeX - Directory lister with hidden file, depth limit and optional file size

Usage:
    treex [PATH] [-a] [--depth N] [--size]

Options:
    -a, --all       Show hidden files
    --depth N       Limit tree depth
    --size          Show file sizes
"""

import os
import sys
import argparse

CONNECT_MID = "├── "
CONNECT_LAST = "└── "
PIPE = "│   "
SPACE = "    "

def format_size(path):
    try:
        size = os.path.getsize(path)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size} {unit}"
            size //= 1024
        return f"{size} TB"
    except Exception:
        return "N/A"

def print_tree(root_path, show_hidden=False, max_depth=None, show_size=False):
    root_path = os.path.abspath(root_path)
    if not os.path.exists(root_path):
        print(f"Error: path does not exist: {root_path}", file=sys.stderr)
        return 1

    print(f"{os.path.basename(root_path)}/")
    _walk(root_path, "", show_hidden, 0, max_depth, show_size)

def _walk(path, prefix, show_hidden, current_depth, max_depth, show_size):
    try:
        with os.scandir(path) as it:
            entries = [e for e in it if show_hidden or not e.name.startswith(".")]
    except PermissionError:
        print(prefix + CONNECT_LAST + "[permission denied]")
        return

    entries.sort(key=lambda e: (not e.is_dir(), e.name.lower()))

    for idx, entry in enumerate(entries):
        is_last = (idx == len(entries) - 1)
        connector = CONNECT_LAST if is_last else CONNECT_MID
        name = entry.name + ("/" if entry.is_dir() else "")
        if show_size and entry.is_file():
            name += f" ({format_size(entry.path)})"
        print(prefix + connector + name)

        if entry.is_dir(follow_symlinks=False):
            if max_depth is None or current_depth + 1 < max_depth:
                extension = SPACE if is_last else PIPE
                _walk(os.path.join(path, entry.name), prefix + extension, show_hidden, current_depth + 1, max_depth, show_size)

def main():
    parser = argparse.ArgumentParser(description="TreeX - Directory lister with optional features")
    parser.add_argument("path", nargs="?", default=os.getcwd(), help="Directory to list")
    parser.add_argument("-a", "--all", action="store_true", help="Show hidden files")
    parser.add_argument("--depth", type=int, default=None, help="Limit tree depth")
    parser.add_argument("--size", action="store_true", help="Show file sizes")
    args = parser.parse_args()

    rc = print_tree(args.path, show_hidden=args.all, max_depth=args.depth, show_size=args.size)
    if rc:
        sys.exit(rc)

if __name__ == "__main__":
    main()
