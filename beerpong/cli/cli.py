"""Command line interface for beerpong."""

import sys

from beerpong.cli.beerpong import beerpong


def main():
    """Run the cli tools.

    Depending on the arguments, it will run the appropriate tool.
    """
    try:
        script_name = sys.argv[1]
        # Remove script name
        del sys.argv[1]
        # Execute known script
    except IndexError:
        script_name = "beerpong"  # Default script if no script name is given
    known_scripts = {
        "beerpong": beerpong,
        "noop": lambda: None,
    }
    if script_name not in known_scripts:
        raise ValueError(
            f"The script {script_name} is unknown,"
            f" please use one of {known_scripts.keys()}"
        )
    known_scripts[script_name]()
