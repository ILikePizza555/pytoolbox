from typing import Any, List, Union, Optional
from pathlib import Path
from enum import Enum, Flag, auto
import re
import sys


_camel_match = re.compile(r"(.)([A-Z][a-z])")


def _to_camel_case(name):
    return _camel_match.sub("\g<1>_\g<2>", name).lower()


class EnumArg(Enum):
    """
    Enum mixin that makes usage with argparse easier.

    Each enum member takes a set of paramters:
        - value: any, the value of the enum member
        - flag: List[str], a list of flags that that should set this value
        - dest: str, an optional string specifying the dest argument in argparse
    """

    def __new__(cls, value: Any, flag: List[str], dest: Optional[str] = None, parser_args: dict = {}):
        if isinstance(value, auto):
            value = cls._generate_next_value_(None, 1, len(cls.__members__), [i.value for k, i in cls.__members__.items()])

        obj = object.__new__(cls)
        obj._value_ = value
        obj.arg_flags = flag

        obj.parser_args = parser_args
        obj.parser_args["dest"] = dest

        return obj

    @classmethod
    def add_to_parser(cls, parser, **kwargs):
        """
        Adds the enum to an argument parser from the argparse library.

        If `dest` exists in args, the member's dest argument is ignored.
        """
        for i in cls:
            for k, v in i.parser_args.values():
                kwargs[k] = v

            parser.add_argument(*i.arg_flags, action="store_const", const=i, **kwargs)


def flag_or_action(flag_type):
    """
    Returns a valid action object to use with add_argument to build flags.

    The action object behaves as follows:
    If a dest already exists in the namespace, then dest will be ORed with itself and const. Otherwise it is set to const.
    If no const is specified, flag_type(0) is used.
    """
    def action_constructor(option_strings,
                           dest,
                           const=None,
                           nargs=0,
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


class FlagArg(Flag):
    def __new__(cls, value, flags: List[str], parser_args={}):
        if isinstance(value, auto):
            value = cls._generate_next_value_(None, 1, len(cls.__members__), [i.value for k, i in cls.__members__.items()])

        obj = object.__new__(cls)
        obj._value_ = value
        obj.flags = flags
        obj.parser_args = parser_args
        return obj

    @classmethod
    def add_to_parser(cls, parser, dest=None, action=None, **kwargs):
        if not dest:
            dest = _to_camel_case(cls.__name__)

        if not action:
            action = flag_or_action(cls)

        for i in cls:
            for k, v in i.parser_args.values():
                kwargs[k] = v

            parser.add_argument(*i.flags, dest=dest, action=action, const=i, **kwargs)


def resolve_paths(paths: List[str], base_dir: Path = Path.cwd(), ignore: List[str] = ["-"]) -> List[Path]:
    """
    Given a list of paths, which may contain patterns, return a list of Path objects to real files.
    """
    real_paths = []

    for p in paths:
        if p not in ignore:
            real_paths.extend(base_dir.glob(p))
        else:
            real_paths.append(Path(p))

    return real_paths


def iterate_input_files(paths: List[Path], default=sys.stdin, **open_args):
    """
    Generator that returns open file handles. If the path is "-", stdin is returned instead.
    """
    if not paths:
        return default

    for path in paths:
        if str(path) == "-":
            yield default
        else:
            f = open(path, **open_args)
            yield f

            if not f.closed:
                f.close()


def add_enum_arguments(enum_type, parser, args: List[tuple], dest=None):
    if not dest:
        dest = _to_camel_case(enum_type.__name__)

    for flag, const, pass_through in args:
        parser.add_argument(flag, action="store_const", dest=dest, const=const, **pass_through)