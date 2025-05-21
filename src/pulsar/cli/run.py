"""
Entry point for Pulsar command line tool.
"""
import click

from pulsar.cli.runner import execute


@click.group()
def cli() -> None:
    """
    (T)est(P)lan (S)uper (REPORT)

    A Testplan tool for report manipulation.
    """
    pass


cli.add_command(execute)


if __name__ == "__main__":
    cli()