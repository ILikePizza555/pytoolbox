from typing import List
import argparse

arg_parser = argparse.ArgumentParser(
    prog="xargs",
    description="Builds and executes commands by converting standard input into arguments to a command."
)
arg_parser.add_argument("test")