from argparse import ArgumentTypeError, ArgumentParser
from sys import argv
from typing import List, NamedTuple


class WindowsInfo(NamedTuple):
    width: int
    height: int


def positive_int(string: str) -> int:
    try:
        nb: int = int(string)
    except:
        raise ArgumentTypeError(f"{string} isn't an integer")
    if nb < 0:
        raise ArgumentTypeError(f"{string} isn't positive")
    return nb


def parse_args(args: List[str] = argv[1:]) -> WindowsInfo:
    parser = ArgumentParser()
    parser.add_argument(
        "--width", type=positive_int, default=800, help="Width of the window"
    )
    parser.add_argument(
        "--height", type=positive_int, default=800, help="Height of the window"
    )
    try:
        arguments = parser.parse_args(args)
    except SystemExit:
        exit(84)
    return WindowsInfo(arguments.width, arguments.height)
