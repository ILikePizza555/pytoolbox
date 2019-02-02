from collections import namedtuple
from typing import List
from pathlib import Path
import getopt

HELP ="""
usage: mv [-i] [-f] SOURCE_FILE TARGET_FILE
   or: mv [-i] [-f] SOURCE_FILE [SOURCE_FILE ...] TARGET_DIR

Renames SOURCE_FILE to TARGET_FILE, or moves SOURCE_FILE(s) to TARGET_DIR.

optional arguments:
-h      Show this help message and exit.
-i      Prompt for confirmation if the destination path exists. Any previous occurance of -f is ignored.
-f      Do not prompt for confirmation if the destination path exists. Any previous occurrence of the -i option is ignored.
"""

Arguments = namedtuple("Arguments", ["mode", "target", "source"])

def parse_args(args: List[str]):
    parsed_args, remainder = getopt.getopt(args, "hif")

    if ('-h', '') in parsed_args:
        print(HELP)
        return 0
    
    mode = None
    if parsed_args:
        mode = parsed_args[-1][0][1]
    
    target = Path(remainder[-1])
    source = map(Path, remainder[:-1])

    return Arguments(mode, target, source)

def _cmd_main(args: List[str]):
    args = parse_args(args)

    # First synopsis is assumed if target_file does not name an exisiting directory
    if not args.target.is_dir():
        args.source[0].rename(args.target)
        return 0

    # Second synopsis
    for s in args.source:
        target = args.target / s.name

        if target.exists() and args.mode == 'i':
            answer = input(f"mv: overwrite {target}?")
            if answer.beginswith("y"):
                s.replace(target)
        elif s.samefile(target):
            print(f"mv: error: {target} points to same location {s}")
        else:
            s.rename(target)