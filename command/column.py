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

`-x`, `--fillrows`
    Fill rows before columns.
"""