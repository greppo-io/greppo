import logging

import click

from .greppo import GreppoApp
from .greppo_server import GreppoServer


@click.command()
@click.argument("command")
@click.argument("path_to_script")
@click.option('--host', default="127.0.0.1", help='Host location for the app.')
@click.option('--port', default="8080", help='Port location for the app.')
def wrap_and_run_script(command, path_to_script, host, port):
    """Run a Greppo COMMAND with PATH_TO_SCRIPT_NAME

    PATH_TO_SCRIPT is the path to the script
    COMMANDS is one of [serve]
    """
    if command == "serve":
        gpo = GreppoApp()
        server = GreppoServer(gr_app=gpo, user_script=path_to_script)

        server.run(host=host, port=int(port))
    else:
        logging.error("Command {} not supported".format(command))


if __name__ == "__main__":
    wrap_and_run_script()
