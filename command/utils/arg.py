from typing import List, Union
from pathlib import Path
import re
import sys


_camel_match = re.compile(r"(.)([A-Z][a-z])")


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
        dest = _camel_match.sub("\g<1>_\g<2>", enum_type.__name__).lower()

    for flag, const, pass_through in args:
        parser.add_argument(flag, action="store_const", dest=dest, const=const, **pass_through)


def flag_or_action(flag_type):
    """
    Returns a valid action object to use with add_argument to build flags.

    The action object behaves as follows:
    If a dest already exists in the namespace, then dest will be ORed with itself and const. Otherwise it is set to const.
    If no const is specified, flag_type(0) is used.
    """
    def action_constructor(option_strings,
                           dest,
                           const,
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