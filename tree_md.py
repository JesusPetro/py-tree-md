"""
tree_md.py

Generate a tree representation of a directory structure.

Dependencies:
    pip install pathspec

Usage:
    python tree_md.py --path /some/folder --max-depth 3 --skip-dirs venv __pycache__ --gitignore --I
"""



from pathlib import Path
import pathspec
import argparse


def load_gitignore_matcher(base_path: str | Path):
    """
    Load a .gitignore file from the given base path and create a matcher.

    Args:
        base_path (str | Path): The directory path where the .gitignore file is located.
                                 Defaults to the current directory if None or empty.

    Returns:
        pathspec.PathSpec | None: A PathSpec matcher object if .gitignore exists,
                                  otherwise None.
    """
    base_path = Path(base_path or ".")
    gi = base_path / ".gitignore"
    if not gi.exists():
        return None
    with gi.open("r", encoding="utf-8") as f:
        return pathspec.PathSpec.from_lines("gitwildmatch", f)

def is_virtual_env_directory(directory: Path) -> bool:
    """
    Determine whether the given directory is a Python virtual environment.

    Args:
        directory (Path): Directory path to check.

    Returns:
        bool: True if the directory appears to be a virtual environment, False otherwise.
    """
    try:
        indicators = [
            directory / 'Scripts' / 'python.exe',
            directory / 'bin' / 'python',
            directory / 'pyvenv.cfg',
            directory / 'Lib' / 'site-packages',
            directory / 'lib' / 'python3.x'
        ]
        
        return any(path.exists() for path in indicators) or \
               any((directory / 'lib').glob('python*')) or \
               (directory / 'pyvenv.cfg').exists()
    except (OSError, PermissionError):
        return False

def normalize_path(filepath: str) -> Path:
    """
    Normalize a file path to an absolute Path object.

    If the provided filepath is None, empty, or does not exist, the function
    returns the parent directory of the current file. If the filepath is relative,
    it is resolved relative to the current file's parent directory.

    Args:
        filepath (str): The file path to normalize. Defaults to __file__.

    Returns:
        Path: An absolute Path object pointing to the file or directory.
    """
    path = Path(filepath)

    if not filepath or not path.exists():
        path = Path(__file__).parent
    elif not path.is_absolute():
        path = (Path(__file__).parent / filepath).resolve()

    return path


def count_folder(filepath: Path) -> int:
    """
    Count the number of subdirectories in a given folder,
    excluding virtual environment directories.

    Args:
        filepath (Path): Path object pointing to the folder to count subdirectories.

    Returns:
        int: Number of subdirectories, excluding virtual environments.
             Returns 0 if the folder cannot be accessed.
    """
    try:
        return sum(
            1 for entry in filepath.iterdir()
            if entry.is_dir()
        )
    except:
        return 0



def tree_md(
    path: str,
    skip_dirs: list[str],
    max_depth: int,
    depth: int = 1,
    gitignore_spec=None,
    indent_str: str = '',
    ignore_hidden: bool = False,
) -> str:
    """
    Generate a tree representation of a directory structure.

    Args:
        path (str): Directory path to process.
        indent_str (str, optional): String used for indentation. Defaults to ''.
        depth (int, optional): Current depth level. Defaults to 1.
        skip_dirs (list[str]): Directories to skip expanding. If ['*'], files beyond level 1 are not shown.
        max_depth (int): Maximum depth to explore.
        gitignore_spec (pathspec.PathSpec, optional): Optional gitignore matcher to exclude files
            and directories according to .gitignore rules. Defaults to None.
        ignore_hidden (bool, optional): If True, hidden files and directories (those starting with '.')
            are ignored. Defaults to False.

    Returns:
        str: Tree structure as a string.
    """


    if skip_dirs is None:
        skip_dirs = []

    if depth > max_depth:
        return ''

    try:
        path = normalize_path(filepath=path)
    except Exception:
        return ''

    tree_str = ''

    try:
        entries = [
            e for e in path.iterdir()
            if not (e.is_dir() and is_virtual_env_directory(e))
        ]

        if ignore_hidden:
            entries = [e for e in entries if not e.name.startswith(".")]
    except (PermissionError, OSError, FileNotFoundError):
        return tree_str


    entries.sort(key=lambda x: (x.is_file(), x.name.lower()))

    if depth == 1:
        tree_str += f'{path.name}/\n'

    if not entries:
        return tree_str

    last_index = count_folder(path) - 1 if depth > 1 and skip_dirs == ['*'] else len(entries) - 1

    for i, entry in enumerate(entries):
        if gitignore_spec:
            rel = entry.relative_to(root).as_posix()

            if entry.is_dir() and not rel.endswith("/"):
                rel += "/"

            if gitignore_spec.match_file(rel):
                continue


        is_last = i == last_index

        connector = '└── ' if is_last else '├── '

        show_entry = True
        if (skip_dirs == ['*'] and depth > 1 and entry.is_file()) or entry.name in skip_dirs:
            show_entry = False

        if show_entry:
            name = f"{entry.name}/" if entry.is_dir() else entry.name
            tree_str += f'{indent_str}{connector}{name}\n'

        if entry.is_dir() and entry.name not in skip_dirs:
            extension = '    ' if is_last else '│   '
            tree_str += tree_md(path= entry, indent_str= indent_str + extension, depth= depth + 1, skip_dirs= skip_dirs, max_depth= max_depth, gitignore_spec=gitignore_spec, ignore_hidden=ignore_hidden)

    return tree_str


if __name__ == "__main__":
    global root
    parser = argparse.ArgumentParser(
        description=__doc__
    )

    parser.add_argument("--path", type = str, default='', help = 'Path to the folder to generate tree (can be absolute or relative)')
    parser.add_argument("--skip-dirs", type = str, nargs="*", default=[''], help = 'Directories to skip')
    parser.add_argument("--max-depth", type = int, default= 100, help = 'Maximum depth')
    parser.add_argument('--output-path', type = str, default='', help='Path to save the output Markdown file')
    parser.add_argument("--gitignore", action="store_true", help="Skip dirs/files from .gitignore")
    parser.add_argument( "-I", "--ignore-hidden", action="store_true", help="Ignore hidden files/folders (names starting with '.')")

    args = parser.parse_args()
    root = normalize_path(args.path)
    skip_dirs = [] if args.skip_dirs else [str(Path(p).resolve().name) for p in args.skip_dirs]

    spec = None

    if args.gitignore: 
        spec = load_gitignore_matcher(args.path or ".")

    output = tree_md(path=args.path, skip_dirs= skip_dirs, max_depth=args.max_depth, gitignore_spec= spec, ignore_hidden=args.ignore_hidden)
    output_path = args.output_path or 'estructura_folderv3.md'

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("```\n" + output + "```")