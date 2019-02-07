from typing import List
from .utils.arg import resolve_paths, iterate_input_files
import argparse

arg_parser = argparse.ArgumentParser(
    prog="head",
    description="Copies each file to the standard output. Copying will end at the nth line in each input file. If no n is given, 10 is assumed."
)
arg_parser.add_argument("-n", type=int, default=10, help="Number of lines to copy to the standard output for each file.")
arg_parser.add_argument("file", nargs="*")

def print_iterator(file_paths):
    first = True

    for path, f in zip(file_paths, iterate_input_files(file_paths)):
        if first:
            print(f"==> {str(path)} <==")
        else:
            print(f"\n==> {str(path)} <==")
        
        yield f

def head(files, n):
    for f in files:
        for _ in range(n):
            print(f.readline(), end='')

def _cmd_main(args: List[str]):
    parsed_args = arg_parser.parse_args(args)

    file_paths = resolve_paths(parsed_args.file)

    if len(file_paths) > 1:
        head(print_iterator(file_paths), parsed_args.n)
    else:
        head(iterate_input_files(file_paths), parsed_args.n)