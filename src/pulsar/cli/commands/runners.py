"""
Implements runner commands of the Pulsar command line tool.
"""
import click

from testplan.report import TestReport
from testplan.exporters.testing import JSONExporter, PDFExporter, XMLExporter
from testplan.common.exporters import ExportContext

from pulsar.cli.utils.command_list import CommandList
from pulsar.cli.utils.actions import ProcessResultAction

runner_commands = CommandList()


class ToJsonAction(ProcessResultAction):
    """
    Writer action for exporting JSON format.
    """

    def __init__(self, output: str) -> None:
        """
        :param output: path to write output to
        """
        self.output = output

    def __call__(self, result: TestReport) -> TestReport:
        """
        :param result: Testplan report to export
        """
        exporter = JSONExporter(json_path=self.output)
        export_context = ExportContext()
        exporter.export(source=result, export_context=export_context)

        return result


@runner_commands.command(name="fromlatency")
def from_latency() -> TestReport:
    """
    Parser command for generating a TestReport.

    :return: A dummy TestReport for demonstration purposes.
    """
    # Replace this with actual logic to generate a TestReport
    return TestReport(name="Latency Report")


@runner_commands.command(name="checklatency")
@click.argument("output", type=click.Path())
def check_latency(output: str) -> ProcessResultAction:
    """
    Writer command for exporting JSON format.

    :param output: path to write output to
    :return: A callable action for processing the result
    """
    return ToJsonAction(output=output)