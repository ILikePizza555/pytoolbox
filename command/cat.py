from typing import List
from .utils.arg import resolve_paths
import argparse
import sys

arg_parser = argparse.ArgumentParser(
    prog="cat",
    description="Reads files in sequence and outputs them to stdout in the same sequence."
)
arg_parser.add_argument("-u", action="store_true", dest="no_delay", help="Writes bytes to stdout without delay.")
arg_parser.add_argument("file", nargs="*")

def iterate_files(file_paths: list, open_args: dict={}):
    if not file_paths:
        yield sys.stdin

    for p in file_paths:
        if p == "-":
            yield sys.stdin
        else:
            f = open(p, *open_args)
            yield f
            
            if not f.closed:
                f.close()

def cat(files, output_func = print):
    for f in files:
        last_str = True

        while last_str:
            last_str = f.readline()
            output_func(last_str)

def _cmd_main(args: List[str]):
    parsed_args = arg_parser.parse_args(args)

    file_paths = resolve_paths(parsed_args.file)
    file_iterator = iterate_files(file_paths)
    
    if not parsed_args.no_delay:
        buffer = []
        cat(file_iterator, buffer.append)
        print("".join(buffer))
    else:
        cat(file_iterator)

    return 0