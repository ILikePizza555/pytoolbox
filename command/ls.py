from typing import List
from enum import Enum, Flag, auto
import argparse
import re

_camel_match = re.compile(r"(.)([A-Z][a-z])")


def add_enum_arguments(enum_type, parser, args: List[tuple], dest=None):
    if not dest:
        dest = _camel_match.sub("\g<1>_\g<2>", enum_type.__name__).lower()

    for flag, const, pass_through in args:
        parser.add_argument(flag, action="store_const", dest=dest, const=const, **pass_through)


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


def flag_or_action(flag_type):
    """
    Returns a valid action object to use with add_argument to build flags.

    The action object behaves as follows:
    If a dest already exists in the namespace, then dest will be ORed with itself and const. Otherwise it is set to const.
    If no const is specified, flag_type(0) is used.
    """
    def action_constructor(option_strings=[],
                           dest=None,
                           nargs=None,
                           const=None,
                           default=None,
                           type=None,
                           choices=None,
                           required=False,
                           help=None,
                           metavar=None):
        def perform_action(parser, namespace, values, option_string=None):
            if hasattr(namespace, dest):
                setattr(namespace, dest, getattr(namespace, dest) | const or flag_type(0))
            else:
                setattr(namespace, dest, const or flag_type(0))

        perform_action.option_strings = option_strings
        perform_action.dest = dest
        perform_action.nargs = nargs
        perform_action.const = const
        perform_action.default = default
        perform_action.type = type
        perform_action.choices = choices
        perform_action.required = required
        perform_action.help = help
        perform_action.metavar = metavar

        return perform_action

    return action_constructor


arg_parser = argparse.ArgumentParser(
    prog="ls",
    description="List directory contents."
)
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


def _cmd_main(args: List[str]):
    parsed_args = arg_parser.parse_args(args)