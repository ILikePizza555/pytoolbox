"""
Implementation of the `column` command from `linux-utils`. This is not a standard unix command
as defined by the IEEE open group standard, but it serves as a useful module for utilities that
format output. Therefore, the command is included.

# SYNOPSIS

`column [options] [file ...]`

# DESCRIPTION

The `column` utility formats its input into multiple columns. It supports three modes:

**columns are filled before rows**
    This is the default mode
**rows are filled before columns**
    This is enabled by the option `-x`, `--fillrows`
**table**
    Determine the number of columns the input contains and create a table.
    This mode is enabled by the option `-t`, `--table`.

# OPTIONS

`-c`, `--output-width` *width*
    Output is formatted to a width specified as number of characters. Input longer than *width* is not truncated by default.

`-d`, `--table-noheadings`
    In table mode, do not print out the header.

`-o`, `--output-separator` *string*
    Specify the columns delimiter. The default is 2 spaces.

`-s`, `--separator` *string*
    Specify a set of of possible input deliminators. In column-first and row-first mode the default is newline. In table mode, the default is all whitespace.

`-t`, `--table`
    Determine the number of columns that the input contains and create a table.

`-N`, `--table-columns` *names*
    Specify the column names by a comma separated list of names. The names are used for the table header.

`--fillcolumns`
    Fill columns before rows. This is the default mode.

`-x`, `--fillrows`
    Fill rows before columns.
"""
from utils.arg import FlagArg
from enum import auto
import argparse
import string
import os

class OutputMode(FlagArg):
    COL_FIRST = auto(), ["--fillcolumns"]
    ROW_FIRST = auto(), ["-x", "--fillrows"]
    TABLE = auto(), ["-t", "--table"]


arg_parser = argparse.ArgumentParser(
    prog="column",
    description="Formats its input into multiple columns."
)
arg_parser.add_argument("file", nargs="*")
arg_parser.add_argument("-c", "--output-width", dest="output_width", type=int, default=None, help="Output is formatted to a width specified as a number of characters.")
arg_parser.add_argument("-o", "--output-separator", dest="output_separator", default="  ", help="Specify the columns delimiter. The default is 2 spaces.")
arg_parser.add_argument("-s", "--separator", dest="separator", type=set, help="Specifies a set of possible input deliminators. In column-first and row-first mode the default is newline. In table mode, the default is all whitespace.")
OutputMode.add_to_parser(arg_parser.add_mutually_exclusive_group())


def _resolve_defaults(parsed_args):
    """
    Resolves default values that depend on the existance of other arguments.
    """
    if not parsed_args.output_width:
        try:
            parsed_args.output_width = os.get_terminal_size()[0]
        except OSError:
            parsed_args.output_width = 0
    
    if not parsed_args.separator:
        if parsed_args.output_mode == OutputMode.TABLE:
            parsed_args.separator = set(string.whitespace)
        else:
            parsed_args.separator = set("\n")