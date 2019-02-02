from typing import List, Union
import argparse
import datetime
import pathlib
import os

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
                             int(seconds))

arg_parser = argparse.ArgumentParser(
    prog="touch",
    description="""
    Touch changes the access or modification times of the specified files. If a file doesn't exist
    and the '-c' option was not specified, then the file will be created.

    By default, touch sets a file's timestamps to the current time.
    """)
arg_parser.add_argument("file", type=pathlib.Path, metavar="FILE", nargs="+", help="The pathname of a file whose times will be modified.")
arg_parser.add_argument("-a", action="store_true", dest="change_access_time", help="Change the access time of FILE.")
arg_parser.add_argument("-c", action="store_false", dest="create_file", help="Do no create FILE if it doesn not exist.")
arg_parser.add_argument("-m", action="store_true", dest="change_modification_time", help="Change the modification time of FILE.")

date_group = arg_parser.add_mutually_exclusive_group()
date_group.add_argument("-r", type=pathlib.Path, dest="ref_path", help="Use the corresponding time of file named by the path instead of the current time.")
date_group.add_argument("-t", type=parse_time_decimal, dest="time", help="Use the specified time instead of the current time.")
date_group.add_argument("-d", type=datetime.datetime.fromisoformat, dest="date_time", help="Use the specified date_time instead of the current time.")

def get_desired_time(file_path: pathlib.Path, 
                     option: Union[pathlib.Path, datetime.datetime, None] = None, 
                     change_access_time: bool = False,
                     change_modification_time: bool = False):
    """
    Returns a 2-tuple that can be passed to os.utime(). If change_access_time is True, then
    the first element of the tuple will use the time set in `option`. If change_modification_time is 
    True, then the second element of the tuple will use the time set in `option`.

    If `option` is a Path, then that file's times will be used. If `option` is a datetime, then `option`
    will be used as the time. If option is None, the current time will be used.
    """

    original_stat = file_path.stat()
    original_times = (original_stat.st_atime, original_stat.st_mtime)

    try:
        ref_stat = option.stat()
        ref_times = (ref_stat.st_atime, ref_stat.st_mtime)
    except AttributeError:
        if not option:
            option = datetime.datetime.now()
        ref_times = (option.timestamp(), option.timestamp())
    
    return (ref_times[0] if change_access_time else original_times[0],
            ref_times[1] if change_modification_time else original_times[1])

def _cmd_main(args: List[str]):
    parsed_args = arg_parser.parse_args(args)

    for file_path in parsed_args.file:
        if not file_path.exists() and parsed_args.create_file:
            f = file_path.open("w+")
            f.close()

            os.utime(file_path)
            continue
        
