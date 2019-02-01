from typing import List
import argparse
import cmds
import sys

PROG_NAME = "toolbox.py"
PROG_VERSION = "0.1.0"
_commands = cmds.load_commands()

def run_command(name: str, args: List[str], **kvargs):
    # TODO: Normalize environment
    status = _commands[name](args, **kvargs)
    
    if status is not None:
        return status
    else:
        return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=PROG_NAME,
        description=f"Executes a command included in this package. Available commands: {list(_commands.values())}",
        epilog=f"Version: {PROG_VERSION}")
    parser.add_argument("cmd_name", metavar="CMD", type=str, help="The name of the command to run.")
    parser.add_argument("cmd_args", metavar="ARG", type=str, nargs="*", help="Arguments to pass to the command.")

    args = parser.parse_args()

    try:
        exit_code = run_command(args.cmd_name, args.cmd_args)
        sys.exit(exit_code)
    except KeyError as e:
        print(f"{PROG_NAME}: error: Invalid command: {e}", file=sys.stderr)
        sys.exit(1)