from typing import List
from pathlib import Path
import argparse
import io


def parse_n(in_str: str) -> int:
    if in_str.startswith("+"):
        return int(in_str[1:])
    if in_str.startswith("-"):
        return -1 * int(in_str[1:])
    return -1 * int(in_str)


arg_parser = argparse.ArgumentParser(
    prog="tail",
    description="Copy the last part of a file."
)
arg_parser.add_argument("-f", action="store_true", dest="wait", help="Do not terminate when the last line has been copied. Copy new lines as they become available until the limit is reached.")
arg_parser.add_argument("file", type=Path, nargs="?")
number_group = arg_parser.add_mutually_exclusive_group()
number_group.add_argument("-c", type=parse_n, metavar="n", dest="n_bytes", help="Read n bytes from the file.")
number_group.add_argument("-n", type=parse_n, metavar="n", dest="n_lines", default=10, help="Read n lines from the file.")


def read_bytes(file, n: int, wait: bool = False):
    """
    Reads n bytes relative to the start of the file.
    If n is negative, then the read will be relative to the end.

    If wait is true, then the function will print bytes as they become available until exactly n bytes are read.
    """

    if not file.seekable():
        raise ValueError("file is not seekable")

    if n < 0:
        file.seek(n, io.SEEK_END)
        n = n * -1

    if not wait:
        print(file.read(n), end="")
    else:
        while n > 0:
            output = file.read(n)

            if not output:
                continue
            else:
                print(output, end="")
                n -= len(output)


def read_lines(file, n: int, wait: bool = False):
    """
    Reads n lines relative to the start of the file.
    If n is negative, then the read will be relative to the end.

    If wait is true, then the function will print lines as they become available until exactly n lines are read.
    """

    if n >= 0:
        lines = [next(file) for _ in range(n)]
    else:
        # TODO: This will only work for smaller files, and use a lot of memory
        lines = list(file)[n:]

    for l in lines:
        print(l)


def _cmd_main(args: List[str]):
    parsed_args = arg_parser.parse_args(args)

    if parsed_args.n_bytes:
        with open(parsed_args.file, mode="rb") as f:
            read_bytes(f, parsed_args.n_bytes)
    elif parsed_args.n_lines:
        with open(parsed_args.file, mode="r") as f:
            read_lines(f, parsed_args.n_lines)

    return 0