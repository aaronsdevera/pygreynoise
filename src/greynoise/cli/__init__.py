"""GreyNoise command line Interface."""

import logging

import click
from click_default_group import DefaultGroup
from click_repl import register_repl

from greynoise.cli import subcommand

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


@click.group(
    cls=DefaultGroup,
    default="query",
    default_if_no_args=False,
    context_settings={"help_option_names": ("-h", "--help")},
)
def main():
    """GreyNoise CLI."""


SUBCOMMAND_FUNCTIONS = [
    subcommand_function
    for subcommand_function in vars(subcommand).values()
    if isinstance(subcommand_function, click.Command)
]

for subcommand_function in SUBCOMMAND_FUNCTIONS:
    main.add_command(subcommand_function)

register_repl(main)
