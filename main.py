import os
import sys
import argparse

CONNECT_MID = "├── "
CONNECT_LAST = "└── "
PIPE = "│   "
SPACE = "    "

def print_tree(root_path, show_hidden=False):
    root_path = os.path.abspath(root_path)
    if not os.path.exists(root_path):
        print(f"Error: path does not exist: {root_path}", file=sys.stderr)
        return 1

    print(f"{os.path.basename(root_path)}/")
    _walk(root_path, "", show_hidden)

def _walk(path, prefix, show_hidden):
    try:
        with os.scandir(path) as it:
            entries = [e for e in it if show_hidden or not e.name.startswith(".")]
    except PermissionError:
        print(prefix + CONNECT_LAST + "[permission denied]")
        return

    # Directories first, then files, alphabetical
    entries.sort(key=lambda e: (not e.is_dir(), e.name.lower()))

    for idx, entry in enumerate(entries):
        is_last = (idx == len(entries) - 1)
        connector = CONNECT_LAST if is_last else CONNECT_MID
        name = entry.name + ("/" if entry.is_dir() else "")
        print(prefix + connector + name)

        if entry.is_dir(follow_symlinks=False):
            extension = SPACE if is_last else PIPE
            _walk(os.path.join(path, entry.name), prefix + extension, show_hidden)

def main():
    parser = argparse.ArgumentParser(description="TreeX - Minimal tree-like directory lister")
    parser.add_argument("path", nargs="?", default=os.getcwd(), help="Directory to list")
    parser.add_argument("-a", "--all", action="store_true", help="Show hidden files")
    args = parser.parse_args()

    rc = print_tree(args.path, show_hidden=args.all)
    if rc:
        sys.exit(rc)

if __name__ == "__main__":
    main()