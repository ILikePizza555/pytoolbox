from typing import List
from pathlib import Path
from command.utils.arg import FlagArg, EnumArg, resolve_paths
from command.column import Table
import argparse
import os


class LongOutputFormat(FlagArg):
    LONG = 1, ["-l"], {"help": "Write output in long format."}
    NO_OWNER = 2, ["-g"], {"help": "Turn on long output, but disable writing the file owner's name and number."}
    NO_GROUP = 4, ["-o"], {"help": "Turn on long ouput, but disable writing the file's group name and number."}
    NUMERIC = 8, ["-n"], {"help": "Turn on long output, but only print the UID and GID."}


class EntryOutput(EnumArg):
    SHOW_HIDDEN = 1, ["-a"], {"help": "Write out all directory entries. Including those starting with '.'. If on Windows, this will also list files marked as hidden."}
    SHOW_HIDDEN_PLUS = 2, ["-A"], {"help": "Same as -a but also lists '.' and '..'. "}


class ShortOutputFormat(EnumArg):
    COLUMNS     = 1, ["-C"], {"help": "Output names sorted in columns."}
    ROWS        = 2, ["-x"], {"help": "Output names sorted in rows."}
    STREAM      = 3, ["-m"], {"help": "Output names in a list seperated by a space and a comma."}
    LIST        = 4, ["-1"], {"help": "Output one name per line."}


class AugmentOutput(EnumArg):
    ALL              = 1, ["-F"], {"help": "Write a slash ('/') immediately after each pathname that is a directory, an asterisk> ('*') after each that is executable, a vertical-line ('|') after each that is a FIFO, and an at-sign ('@') after each that is a symbolic link. For other file types, other symbols may be written."}
    ONLY_DIRECTORIES = 2, ["-p"], {"help": "Write a slash after each filename that's a directory."}


class DereferenceBehavior(EnumArg):
    COMMAND_LINE = 1, ["-H"], {"help": "Evaluate the file information for all links specified on the command line to be that of the file pointed to by the link. However, the name of the link will be printed and not the the file referenced by the link."}
    ALL          = 2, ["-L"], {"help": "Evaluate the file information for all links encountered to be that of the file pointed to by the link. However, the name of the link will be printed and not the file reference by the link."}


class SortBehavior(EnumArg):
    FILE_SIZE       = 1, ["-S"], {"help": "List the files in order of file size."}
    ORDER           = 2, ["-f"], {"help": "List the files in the order they appear in the directory."}
    TIME_MODIFIED   = 3, ["-t"], {"help": "List the files in order of time modified."}


class TimeBehavior(EnumArg):
    TIME_MODIFIED = 1, ["--mtime"]
    CTIME         = 2, ["-c"]
    TIME_ACCESSED = 3, ["-u"]


arg_parser = argparse.ArgumentParser(
    prog="ls",
    description="List directory contents."
)
arg_parser.add_argument("paths", nargs="*", default=["."])
arg_parser.add_argument("-i", action="store_true", dest="write_serial", help="For each file write out the file's serial number.")
arg_parser.add_argument("-k", action="store_true", dest="kilo_blocks", help="Set the block size to 1024 bytes.")
arg_parser.add_argument("-q", action="store_true", dest="only_printable", help="Force each instance of non-printable filename characters and <tab> to be written as '?'")
arg_parser.add_argument("-r", action="store_true", dest="reverse_order", help="Reverse the order of the sort.")
arg_parser.add_argument("-s", action="store_true", dest="display_blocks", help="Indicate the total number of system blocks consumed by each file displayed.")

recurse_group = arg_parser.add_mutually_exclusive_group()
recurse_group.add_argument("-R", action="store_true", dest="recurse", help="Descend into all subdirectories encountered."),
recurse_group.add_argument("-d", action="store_false", default=False, dest="recurse", help="Treat subdirectories no differently.")

LongOutputFormat.add_to_parser(arg_parser.add_mutually_exclusive_group())
EntryOutput.add_to_parser(arg_parser.add_mutually_exclusive_group())
ShortOutputFormat.add_to_parser(arg_parser.add_mutually_exclusive_group())
AugmentOutput.add_to_parser(arg_parser.add_mutually_exclusive_group())
DereferenceBehavior.add_to_parser(arg_parser.add_mutually_exclusive_group())
SortBehavior.add_to_parser(arg_parser.add_mutually_exclusive_group())
TimeBehavior.add_to_parser(arg_parser.add_mutually_exclusive_group())


def short_column_out(items: List[Path], formatter=lambda p: p.name):
    t = Table.create_column_first(map(formatter, items), os.get_terminal_size()[0], 2)
    t.print_table()


def short_row_out(items: List[Path], formatter=lambda p: p.name):
    t = Table.create_row_first(items, os.get_terminal_size()[0], 2)
    t.print_table()


def short_stream_out(items: List[Path], formatter=lambda p: p.name):
    print(", ".join(map(formatter, items)))


def short_list_out(items: List[Path], formatter=lambda p: p.name):
    for i in items:
        print(formatter(i))


_PRINT_FUNC_MAP = {
    ShortOutputFormat.COLUMNS: short_column_out,
    ShortOutputFormat.ROWS: short_row_out,
    ShortOutputFormat.STREAM: short_stream_out,
    ShortOutputFormat.LIST: short_list_out,
}


def ls(paths: List[Path], print_func, show_hidden=False, show_dots=False, recurse=False):
    for path in paths:
        if len(paths) > 1 or recurse:
            print(f"{path}:")

        if path.is_dir():
            items = list(path.iterdir())

            print_func(items)

            if recurse:
                ls([x for x in items if x.is_dir()], print_func, recurse)


def _cmd_main(args: List[str]):
    parsed_args = arg_parser.parse_args(args)

    if parsed_args.short_output_format:
        print_func = _PRINT_FUNC_MAP[parsed_args.short_output_format]
    else:
        print_func = short_column_out

    paths = resolve_paths(parsed_args.paths, ignore=["."])
    ls(paths,
       print_func,
       show_hidden=bool(parsed_args.entry_output),
       show_dots=bool(parsed_args.entry_output == EntryOutput.SHOW_HIDDEN_PLUS),
       recurse=parsed_args.recurse)

    return 0