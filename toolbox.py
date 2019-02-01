from typing import List
import argparse
import cmds
import sys

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
        description=f"Executes a command included in this package. Available commands: {list(_commands.values())}"
        )
    parser.add_argument("cmd_name", metavar="CMD", type=str, nargs=1, help="The name of the command to run.")
    parser.add_argument("cmd_args", metavar="ARG", type=str, nargs='*', help="Arguments to pass to the command.")

    args = parser.parse_args(sys.argv)

    exit_code = run_command(args.cmd_name, args.cmd_args)
    sys.exit(exit_code)