from typing import Sequence, Union

import click

from pulsar.cli.commands import runner_commands
from pulsar.cli.utils.actions import ProcessResultAction, ParseSingleAction


@click.group(name="execute", chain=True)
def execute() -> None:
    """
    Execute a type of test for Pulsar toolkit.
    """
    pass


@execute.result_callback()
def run_actions(
    actions: Sequence[Union[ParseSingleAction, ProcessResultAction]]
) -> None:
    """
    Result callback for `execute` command.

    :param actions: sequence of a single parser and, possibly, multiple
        processor actions.
    """
    parse, *processors = actions

    if not (
        isinstance(parse, ParseSingleAction)
        and all((isinstance(p, ProcessResultAction) for p in processors))
    ):
        raise click.UsageError(
            "convert needs a single parser of the form `from*` and can have"
            " multiple processors or targets of the form `to*` or `display`"
        )

    result = parse()

    for process in processors:
        result = process(result)


runner_commands.register_to(execute)
# execute.add_command(runner_commands)
