from typing import List
import argparse
import datetime
import pathlib

def parse_time_decimal(time: str):
    """Parses the string into a datetime according to [[CC]YY]MMDDhhmm[.SS]"""
    seconds = 0
    century = 0
    year = 0

    if "." in time:
        time, seconds = time.split(".", 1)
    
    if len(time) == 12:
        century = int(time[:2])
        time = time[2:]

    if len(time) == 10:
        year = int(time[:2])
        time = time[2:]

        if not century:
            if year >= 69 and year <= 99:
                century = 19
            if year >= 0 and year <= 68:
                century = 20
        
        year += century * 100

    if not year:
        year = datetime.date.today().year
    
    return datetime.datetime(year, 
                             int(time[:2]), 
                             int(time[2:4]), 
                             int(time[4:6]), 
                             int(time[6:8]),
                             seconds)

arg_parser = argparse.ArgumentParser(
    prog="touch",
    description="""
    Touch changes the access or modification times of the specified files. If a file doesn't exist
    and the '-c' option was not specified, then the file will be created.

    By default, touch sets a file's timestamps to the current time.
    """)
arg_parser.add_argument("FILE", nargs="+", help="The pathname of a file whose times will be modified.")
arg_parser.add_argument("-a", action="store_true", dest="change_access_time", help="Change the access time of FILE.")
arg_parser.add_argument("-c", action="store_false", dest="create_file", help="Do no create FILE if it doesn not exist.")
arg_parser.add_argument("-m", action="store_true", dest="change_modification_time", help="Change the modification time of FILE.")

date_group = arg_parser.add_mutually_exclusive_group()
date_group.add_argument("-r", type=pathlib.Path, dest="ref_path", help="Use the corresponding time of file named by the path instead of the current time.")
date_group.add_argument("-t")

def _cmd_main(args: List[str]):
    pass