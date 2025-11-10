#!/usr/bin/env python3
import os
import sys
import argparse

CONNECT_MID = "├── "
CONNECT_LAST = "└── "
PIPE = "│   "
SPACE = "    "

def format_size_bytes(size_bytes):
    size = size_bytes
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size} {unit}"
        size //= 1024
    return f"{size} TB"

def format_size(path):
    try:
        if os.path.isfile(path):
            size = os.path.getsize(path)
        else:
            size = 0
            for root, dirs, files in os.walk(path):
                for f in files:
                    try:
                        size += os.path.getsize(os.path.join(root, f))
                    except Exception:
                        continue
        return format_size_bytes(size)
    except Exception:
        return "N/A"

def format_lines(path):
    try:
        with open(path, 'r', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return "N/A"

def print_tree(root_path, show_hidden=False, max_depth=None, show_size=False, show_lines=False):
    root_path = os.path.abspath(root_path)
    if not os.path.exists(root_path):
        print(f"Error: path does not exist: {root_path}", file=sys.stderr)
        return 1

    print(f"{os.path.basename(root_path)}/")
    _walk(root_path, "", show_hidden, 0, max_depth, show_size, show_lines)

def _walk(path, prefix, show_hidden, current_depth, max_depth, show_size, show_lines):
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
        if show_size:
            name += f" ({format_size(entry.path)})"
        if entry.is_file() and show_lines:
            name += f" [{format_lines(entry.path)} lines]"
        print(prefix + connector + name)

        if entry.is_dir(follow_symlinks=False):
            if max_depth is None or current_depth + 1 < max_depth:
                extension = SPACE if is_last else PIPE
                _walk(os.path.join(path, entry.name), prefix + extension, show_hidden, current_depth + 1, max_depth, show_size, show_lines)

def summary_stats(path, show_hidden=False):
    total_files = 0
    total_dirs = 0
    total_size = 0
    total_lines = 0
    hidden_count = 0

    for root, dirs, files in os.walk(path):
        hidden_count += sum(1 for d in dirs if d.startswith(".") and show_hidden)
        hidden_count += sum(1 for f in files if f.startswith(".") and show_hidden)
        total_dirs += len(dirs)
        total_files += len(files)
        for f in files:
            fp = os.path.join(root, f)
            try:
                total_size += os.path.getsize(fp)
            except Exception:
                continue
            try:
                with open(fp, 'r', errors='ignore') as file:
                    total_lines += sum(1 for _ in file)
            except Exception:
                continue

    return total_files, total_dirs, total_size, total_lines, hidden_count

def print_summary(path, show_hidden=False):
    total_files, total_dirs, total_size, total_lines, hidden_count = summary_stats(path, show_hidden)
    print("\n--- Summary ---")
    print(f"dosya sayısı: {total_files}")
    print(f"klasör sayısı: {total_dirs}")
    print(f"toplam boyut: {format_size_bytes(total_size)}")
    print(f"toplam satır: {total_lines}")
    print(f"gizli dosya/klasör sayısı: {hidden_count}")

def main():
    parser = argparse.ArgumentParser(description="TreeX - Directory lister with optional features")
    parser.add_argument("path", nargs="?", default=os.getcwd(), help="Directory to list")
    parser.add_argument("-a", "--all", action="store_true", help="Show hidden files")
    parser.add_argument("--depth", type=int, default=None, help="Limit tree depth")
    parser.add_argument("--size", action="store_true", help="Show file and folder sizes")
    parser.add_argument("--lines", action="store_true", help="Show number of lines in files")
    parser.add_argument("--summary", action="store_true", help="Show summary statistics")
    args = parser.parse_args()

    rc = print_tree(args.path, show_hidden=args.all, max_depth=args.depth, show_size=args.size, show_lines=args.lines)
    if rc:
        sys.exit(rc)

    if args.summary:
        print_summary(args.path, show_hidden=args.all)

if __name__ == "__main__":
    main()
