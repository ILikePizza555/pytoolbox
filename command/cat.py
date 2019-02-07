from typing import List
from .utils.arg import resolve_paths, iterate_input_files
import argparse
import sys

arg_parser = argparse.ArgumentParser(
    prog="cat",
    description="Reads files in sequence and outputs them to stdout in the same sequence."
)
arg_parser.add_argument("-u", action="store_true", dest="no_delay", help="Writes bytes to stdout without delay.")
arg_parser.add_argument("file", nargs="*")

def cat(files, output_func = print):
    for f in files:
        last_str = True

        while last_str:
            last_str = f.readline()
            output_func(last_str)

def _cmd_main(args: List[str]):
    parsed_args = arg_parser.parse_args(args)

    file_paths = resolve_paths(parsed_args.file)
    file_iterator = iterate_input_files(file_paths, mode="r")
    
    if not parsed_args.no_delay:
        buffer = []
        cat(file_iterator, buffer.append)
        print("".join(buffer))
    else:
        cat(file_iterator)

    return 0