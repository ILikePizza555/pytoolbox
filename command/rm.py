from collections import namedtuple
from typing import List
from pathlib import Path
import getopt
import sys

HELP = """
usage: rm [-f] [-i] [-R] [-r] file [file ...]

Removes all specified files.

optional arguments:
-h      Print this help message
-f      Do not prompt for confirmation. Do not write error messages or modify the exit status in the case of nonexistant operands.
-i      Prompt for confirmation.
-R      Remove heirarchies
-r      Same as -R
"""

Arguments = namedtuple("Arguments", ["mode", "recurse", "files"])

def parse_args(args: List[str]):
    if not args:
        return None

    parsed_args, remainder = getopt.getopt(args, "hfiRr")
    parsed_args = [x[0] for x in parsed_args]

    if '-h' in parsed_args:
        print(HELP)
        return None
    
    return Arguments(
        next((i[1] for i in reversed(parsed_args) if i == "-f" or i == "-i"), None),
        "-r" in parsed_args or "-R" in parsed_args,
        list(map(Path, remainder))
    )

def remove(files: List[Path], mode: str, recurse: bool):
    for path in files:
        if not path.exists():
            if mode != "f":
                print(f"rm: {path} not found", file=sys.stderr)
        elif path.is_dir():
            if not recurse:
                print(f"rm: cannot remove {path}: is a directory", file=sys.stderr)
            elif mode == "i":
                answer = input(f"rm: descend into directory {path}?")
                if answer.startswith("y"):
                    remove(list(path.iterdir()), mode, recurse)
                    path.rmdir()
            else:
                remove(list(path.iterdir()), mode, recurse)
                path.rmdir()
        elif mode == "i":
            answer = input(f"rm: remove file {path}?")
            if answer.startswith("y"):
                path.unlink()
        else:
            path.unlink()

def _cmd_main(args: List[str]):
    parsed_args = parse_args(args)
    if not parsed_args:
        return 0

    remove(parsed_args.files, parsed_args.mode, parsed_args.recurse)

    
