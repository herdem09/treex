#!/usr/bin/env python3
import os
import sys
import argparse
from collections import Counter

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
            return os.path.getsize(path)
        else:
            size = 0
            for root, dirs, files in os.walk(path):
                for f in files:
                    try:
                        size += os.path.getsize(os.path.join(root, f))
                    except Exception:
                        continue
            return size
    except Exception:
        return 0

def format_lines(path):
    try:
        with open(path, 'r', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def print_tree(root_path, show_hidden=False, max_depth=None, show_size=False, show_lines=False, ignore_types=None):
    root_path = os.path.abspath(root_path)
    if not os.path.exists(root_path):
        print(f"Error: path does not exist: {root_path}", file=sys.stderr)
        return 1
    print(f"{os.path.basename(root_path)}/")
    _walk(root_path, "", show_hidden, 0, max_depth, show_size, show_lines, ignore_types)

def _walk(path, prefix, show_hidden, current_depth, max_depth, show_size, show_lines, ignore_types):
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

        if entry.is_file():
            if ignore_types and any(entry.name.endswith(ext) for ext in ignore_types):
                continue
            if show_size:
                name += f" ({format_size_bytes(format_size(entry.path))})"
            if show_lines:
                name += f" [{format_lines(entry.path)} lines]"

        print(prefix + connector + name)

        if entry.is_dir(follow_symlinks=False):
            if max_depth is None or current_depth + 1 < max_depth:
                extension = SPACE if is_last else PIPE
                _walk(os.path.join(path, entry.name), prefix + extension, show_hidden, current_depth + 1, max_depth, show_size, show_lines, ignore_types)

def summary_stats(path, show_hidden=False, ignore_types=None):
    total_files = 0
    total_dirs = 0
    total_size = 0
    total_lines = 0
    hidden_count = 0
    max_file_size = 0
    min_file_size = None
    max_dir_size = 0
    min_dir_size = None
    max_lines = 0

    for root, dirs, files in os.walk(path):
        hidden_count += sum(1 for d in dirs if d.startswith(".") and show_hidden)
        hidden_count += sum(1 for f in files if f.startswith(".") and show_hidden)
        total_dirs += len(dirs)

        for f in files:
            if ignore_types and any(f.endswith(ext) for ext in ignore_types):
                continue
            total_files += 1
            fp = os.path.join(root, f)
            try:
                size = os.path.getsize(fp)
                total_size += size
                if size > max_file_size:
                    max_file_size = size
                if min_file_size is None or size < min_file_size:
                    min_file_size = size
                lines = format_lines(fp)
                total_lines += lines
                if lines > max_lines:
                    max_lines = lines
            except Exception:
                continue

        for d in dirs:
            dp = os.path.join(root, d)
            try:
                size = format_size(dp)
                if size > max_dir_size:
                    max_dir_size = size
                if min_dir_size is None or size < min_dir_size:
                    min_dir_size = size
            except Exception:
                continue

    avg_file_size = total_size // total_files if total_files else 0

    return {
        "total_files": total_files,
        "total_dirs": total_dirs,
        "total_size": total_size,
        "total_lines": total_lines,
        "hidden_count": hidden_count,
        "max_file_size": max_file_size,
        "min_file_size": min_file_size or 0,
        "max_dir_size": max_dir_size,
        "min_dir_size": min_dir_size or 0,
        "avg_file_size": avg_file_size,
        "max_lines": max_lines
    }

def print_summary(stat_dict):
    print("\n--- Summary ---")
    print(f"Total files: {stat_dict['total_files']}")
    print(f"Total directories: {stat_dict['total_dirs']}")
    print(f"Total size: {format_size_bytes(stat_dict['total_size'])}")
    print(f"Largest file size: {format_size_bytes(stat_dict['max_file_size'])}")
    print(f"Smallest file size: {format_size_bytes(stat_dict['min_file_size'])}")
    print(f"Largest directory size: {format_size_bytes(stat_dict['max_dir_size'])}")
    print(f"Smallest directory size: {format_size_bytes(stat_dict['min_dir_size'])}")
    print(f"Average file size: {format_size_bytes(stat_dict['avg_file_size'])}")
    print(f"Longest file lines: {stat_dict['max_lines']}")

def extension_distribution(path, show_hidden=False, ignore_types=None):
    ext_counter = Counter()
    for root, dirs, files in os.walk(path):
        for f in files:
            if ignore_types and any(f.endswith(ext) for ext in ignore_types):
                continue
            if not show_hidden and f.startswith("."):
                continue
            ext = os.path.splitext(f)[1] or "NO_EXT"
            ext_counter[ext] += 1
    return ext_counter

def print_extdist(ext_counter):
    print("\n--- Extension Distribution ---")
    for ext, count in ext_counter.most_common():
        print(f"{ext}: {count}")

def main():
    parser = argparse.ArgumentParser(description="TreeX - Directory lister with optional features")
    parser.add_argument("path", nargs="?", default=os.getcwd(), help="Directory to list")
    parser.add_argument("-a", "--all", action="store_true", help="Show hidden files")
    parser.add_argument("--depth", type=int, default=None, help="Limit tree depth")
    parser.add_argument("--size", action="store_true", help="Show file and folder sizes")
    parser.add_argument("--lines", action="store_true", help="Show number of lines in files")
    parser.add_argument("--ignoretype", "-it", nargs="*", default=None, help="Ignore specified file types (.ext)")
    parser.add_argument("--summary", action="store_true", help="Show summary statistics")
    parser.add_argument("--extdist", "-ed", action="store_true", help="Show extension distribution")
    args = parser.parse_args()

    rc = print_tree(args.path, show_hidden=args.all, max_depth=args.depth, show_size=args.size,
                    show_lines=args.lines, ignore_types=args.ignoretype)
    if rc:
        sys.exit(rc)

    if args.summary:
        stat_dict = summary_stats(args.path, show_hidden=args.all, ignore_types=args.ignoretype)
        print_summary(stat_dict)

    if args.extdist:
        ext_counter = extension_distribution(args.path, show_hidden=args.all, ignore_types=args.ignoretype)
        print_extdist(ext_counter)

if __name__ == "__main__":
    main()
