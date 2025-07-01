import os


def print_tree(start_path='.', max_depth=2, prefix=''):
    try:
        items = os.listdir(start_path)
    except PermissionError:
        return
    for index, item in enumerate(items):
        full_path = os.path.join(start_path, item)
        connector = '└── ' if index == len(items) - 1 else '├── '
        print(f"{prefix}{connector}{item}")
        if os.path.isdir(full_path) and max_depth > 1:
            extension = '    ' if index == len(items) - 1 else '│   '
            print_tree(full_path, max_depth - 1, prefix + extension)


print_tree('.', max_depth=2)
