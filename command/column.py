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
from command.utils.arg import FlagArg
from enum import auto
from typing import Any, List
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


class Table():
    class RowIter():
        def __init__(self, table, row_index):
            self._n = 0
            self.table = table
            self.row_index = row_index

        def __iter__(self):
            self._n = 0
            return self

        def __next__(self):
            if self._n < self.table.col_num:
                try:
                    rv = self.table.columns[self._n][self.row_index]
                    self._n += 1
                    return rv
                except IndexError:
                    raise StopIteration
            else:
                raise StopIteration

        def __len__(self):
            return sum(1 for x in self)

    def __init__(self, columns: List[List[Any]] = [[]]):
        self.columns: List[List[Any]] = columns
        self._rows = max([len(x) for x in columns], default=1) or 1

    def _take(self, n, start=0):
        rv = []

        while len(rv) < n and start < self.col_num:
            if self.columns[start]:
                rv.append(self.columns[start].pop(0))

            if not self.columns[start]:
                del self.columns[start]

        return rv

    def _compress_columns(self, row_count):
        for i_col in range(self.col_num):
            n = row_count - len(self.columns[i_col])
            self.columns[i_col].extend(self._take(n, i_col + 1))

    @property
    def col_num(self):
        return len(self.columns)

    @property
    def row_num(self):
        return self._rows

    @property
    def rows(self):
        return tuple(Table.RowIter(self, i) for i in range(self.row_num))
    
    def append_to_column(self, item):
        """
        Adds an item to the table, filling up the last column before making a new one
        """
        if len(self.columns[-1]) == self.row_num:
            self.columns.append([])
        self.columns[-1].append(item)

    def add_row(self, compress_columns=True):
        """
        Adds a new row to the table. If compress_columns is true, then existings columns will be compressed to fill the new row.
        """
        self._rows += 1

        if compress_columns:
            self._compress_columns(self._rows)

    @classmethod
    def create_column_first(cls, input, max_row_width: int, column_padding: int = 0, length_function=len):
        """
        Creates a new table from the input by filling columns first. 
        """
        table = cls()

        for item in input:
            last_row = table.rows[-1]

            # Calculate the new row size to see if we need to compress
            last_row_size = sum(length_function(x) + column_padding for x in last_row)
            new_row_size = length_function(item) + last_row_size

            # Continiously add rows until we fit or only have one column
            while new_row_size > max_row_width and table.col_num > 1:
                table.add_row()
            
            table.append_to_column(item)