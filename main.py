import os
import sys

CONNECT_MID = "├── "
CONNECT_LAST = "└── "
PIPE = "│   "
SPACE = "    "

def print_tree(root_path):
    root_path = os.path.abspath(root_path)
    if not os.path.exists(root_path):
        print(f"Error: path does not exist: {root_path}", file=sys.stderr)
        return 1

    print(f"{os.path.basename(root_path)}/")
    _walk(root_path, "")

def _walk(path, prefix):
    try:
        with os.scandir(path) as it:
            entries = [entry for entry in it]
    except PermissionError:
        print(prefix + CONNECT_LAST + "[permission denied]")
        return

    # sort: directories first, then files, both alphabetically
    entries.sort(key=lambda e: (not e.is_dir(), e.name.lower()))

    for idx, entry in enumerate(entries):
        is_last = (idx == len(entries) - 1)
        connector = CONNECT_LAST if is_last else CONNECT_MID
        name = entry.name + ("/" if entry.is_dir() else "")
        print(prefix + connector + name)

        if entry.is_dir(follow_symlinks=False):
            extension = SPACE if is_last else PIPE
            _walk(os.path.join(path, entry.name), prefix + extension)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    rc = print_tree(path)
    if rc:
        sys.exit(rc)