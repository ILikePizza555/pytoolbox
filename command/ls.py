from typing import List
from enum import Enum, Flag, auto
from pathlib import Path
from utils.arg import add_enum_arguments, flag_or_action
import argparse


class LongOutputMethod(Flag):
    SHORT = 0
    LONG = auto()
    NO_OWNER = auto()
    NO_GROUP = auto()
    NUMERIC = auto()

    @classmethod 
    def add_argument(cls, parser, name: str, const, dest="output_method", **kwargs):
        return parser.add_argument(name, action=flag_or_action(cls), dest=dest, const=const, **kwargs)


class EntryOutput(Enum):
    REGULAR = 0
    SHOW_HIDDEN = 1
    SHOW_HIDDEN_PLUS = 2


class ShortOutputFormat(Enum):
    COLUMNS = 0
    ROWS = 1
    STREAM = 2
    LIST = 3


class AugmentOutput(Enum):
    ALL = 0
    ONLY_DIRECTORIES = 1


class DereferenceBehavior(Enum):
    COMMAND_LINE = 0
    ALL = 1


class SortBehavior(Enum):
    FILE_SIZE = 0
    ORDER = 1
    TIME_MODIFIED = 2


class TimeBehavior(Enum):
    TIME_MODIFIED = 0
    CTIME = 1
    TIME_ACCESSED = 2


arg_parser = argparse.ArgumentParser(
    prog="ls",
    description="List directory contents."
)
arg_parser.add_argument("paths", type=Path, nargs="*", default=Path.cwd())
arg_parser.add_argument("-i", action="store_true", dest="write_serial", help="For each file write out the file's serial number.")
arg_parser.add_argument("-k", action="store_true", dest="kilo_blocks", help="Set the block size to 1024 bytes.")
arg_parser.add_argument("-q", action="store_true", dest="only_printable", help="Force each instance of non-printable filename characters and <tab> to be written as '?'")
arg_parser.add_argument("-r", action="store_true", dest="reverse_order", help="Reverse the order of the sort.")
arg_parser.add_argument("-s", action="store_true", dest="display_blocks", help="Indicate the total number of system blocks consumed by each file displayed.")

LongOutputMethod.add_argument(arg_parser, "-g", LongOutputMethod.LONG | LongOutputMethod.NO_OWNER, help="Turn on long output, but disable writing the file owner's name and number.")
LongOutputMethod.add_argument(arg_parser, "-l", LongOutputMethod.LONG, help="Write output in long format.")
LongOutputMethod.add_argument(arg_parser, "-n", LongOutputMethod.LONG | LongOutputMethod.NUMERIC, help="Turn on long output, but only print the UID and GID.")
LongOutputMethod.add_argument(arg_parser, "-o", LongOutputMethod.LONG | LongOutputMethod.NO_GROUP, help="Turn on long ouput, but disable writing the file's group name and number.")

add_enum_arguments(
    EntryOutput,
    arg_parser.add_mutually_exclusive_group(),
    [
        ("-a", EntryOutput.SHOW_HIDDEN, {"help": "Write out all directory entries. Including those starting with '.'. If on Windows, this will also list files marked as hidden."}),
        ("-A", EntryOutput.SHOW_HIDDEN_PLUS, {"help": "Same as -a but also lists '.' and '..'. "})
    ]
)

add_enum_arguments(
    ShortOutputFormat,
    arg_parser.add_mutually_exclusive_group(),
    [
        ("-C", ShortOutputFormat.COLUMNS, {"help": "Output names sorted in columns."}),
        ("-m", ShortOutputFormat.STREAM, {"help": "Output names in a list seperated by a space and a comma."}),
        ("-x", ShortOutputFormat.ROWS, {"help": "Output names sorted in rows."}),
        ("-1", ShortOutputFormat.LIST, {"help": "Output one name per line."})
    ]
)

add_enum_arguments(
    AugmentOutput,
    arg_parser.add_mutually_exclusive_group(),
    [
        ("-F", AugmentOutput.ALL, {"help": "Write a slash ('/') immediately after each pathname that is a directory, an asterisk> ('*') after each that is executable, a vertical-line ('|') after each that is a FIFO, and an at-sign ('@') after each that is a symbolic link. For other file types, other symbols may be written."})
        ("-p", AugmentOutput.ONLY_DIRECTORIES, {"help": "Write a slash after each filename that's a directory."})
    ]
)

add_enum_arguments(
    DereferenceBehavior,
    arg_parser.add_mutually_exclusive_group(),
    [
        ("-H", DereferenceBehavior.COMMAND_LINE, {"help": "Evaluate the file information for all links specified on the command line to be that of the file pointed to by the link. However, the name of the link will be printed and not the the file referenced by the link."})
        ("-L", DereferenceBehavior.ALL, {"help": "Evaluate the file information for all links encountered to be that of the file pointed to by the link. However, the name of the link will be printed and not the file reference by the link."})
    ]
)

recurse_group = arg_parser.add_mutually_exclusive_group()
recurse_group.add_argument("-R", action="store_true", dest="recurse", help="Descend into all subdirectories encountered.")
recurse_group.add_argument("-d", action="store_false", default=False, dest="recurse", help="Treat subdirectories no differently.")

add_enum_arguments(
    SortBehavior,
    arg_parser.add_mutually_exclusive_group(),
    [
        ("-S", SortBehavior.FILE_SIZE, {"help": "List the files in order of file size."}),
        ("-f", SortBehavior.ORDER, {"help": "List the files in the order they appear in the directory."}),
        ("-t", SortBehavior.TIME_MODIFIED, {"help": "List the files in order of time modified."})
    ]
)

add_enum_arguments(
    TimeBehavior,
    arg_parser.add_mutually_exclusive_group(),
    [
        ("-c", TimeBehavior.CTIME),
        ("-u", TimeBehavior.TIME_ACCESSED)
    ]
)

def _cmd_main(args: List[str]):
    parsed_args = arg_parser.parse_args(args)