import logging

import click
from .greppo import GreppoApp
from .greppo_server import GreppoServer


@click.command()
@click.argument("command")
@click.argument("path_to_script")
def wrap_and_run_script(command, path_to_script: str):
    """Run a Greppo COMMAND with PATH_TO_SCRIPT_NAME

    PATH_TO_SCRIPT is the path to the script
    COMMANDS is one of [serve]
    """
    if command == "serve":
        gpo = GreppoApp()
        server = GreppoServer(gr_app=gpo, user_script=path_to_script)

        server.run()
    else:
        logging.error("Command {} not supported".format(command))


if __name__ == "__main__":
    wrap_and_run_script()
