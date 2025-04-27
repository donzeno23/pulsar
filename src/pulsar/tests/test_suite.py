from rich import print as rprint

from testplan.testing.multitest import testsuite, testcase
from testplan.common.entity.base import Runnable
from testplan.testing.result import Result

from pulsar.utils.loader import load_stage_modules
from pulsar.stages.factory import setup_stages
from pulsar.stages import get_logs, send_messages


def print_stages(stages):
    """Pretty prints the list of stages to be executed"""
    rprint("[bold blue]Stages to be executed:[/bold blue]")
    for i, stage in enumerate(stages, 1):
        rprint(f"[green]{i}.[/green] [yellow]{stage.name}[/yellow]")


@testsuite(name="Test Suite for Pulsar Stage")
class StageTestSuite(object):
    """
    A test suite for the Pulsar stage.
    """
    # def __init__(self):
    #     self.stages = load_stage_modules()

    # NOTE: The setup method needs to define env, result, otherwise get error:
    # AttributeError: 'MethodSignatureMismatch' object has no attribute 'flattened_logs'
    def setup(self, env, result):
        """
        Set up the test suite by loading the stage modules.
        """
        rprint("[bold blue]Setting up the test suite...[/bold blue]")
        result.log("Setting up the test suite...")

        rprint("[bold blue]Loading the stage modules...[/bold blue]")
        result.log("Loading the stage modules...")
        # self.stages = load_stage_modules()
        self.stages = setup_stages()

        import pdb; pdb.set_trace()

        rprint("[bold green]Pulsar stage modules loaded successfully![/bold green]")
        result.log("Pulsar stage modules loaded successfully!")

        print_stages(self.stages)

        self.stages[0].setup(env=env, result=result)
        # get_logs.setup()

        self.stages[1].setup(env=env, result=result)
        # send_messages.setup()

    @testcase
    def test_run(self, env, result):
        result.log("Running the test suite...")
        rprint("[bold blue]Running the test suite...[/bold blue]")
        rprint("[bold blue]Running the stages...[/bold blue]")
        get_logs.run(env=env, result=result)
        rprint("[bold blue]Running the send_messages stage...[/bold blue]")
        send_messages.run(env=env, result=result)

    def teardown(self, env, result):  
        rprint("[bold red]Tearing down the test suite...[/bold red]")
        rprint("[bold red]Tearing down the stages...[/bold red]")        
        get_logs.teardown()
        send_messages.teardown()


@testsuite(name="Another Test Suite for Pulsar Stage")
class StageTestSuite2(object):
    """
    Another test suite for the Pulsar stage.
    """
    def setup(self, env, result):
        """
        Set up the test suite by loading the stage modules.
        """
        rprint("[bold blue]Setting up the test suite...[/bold blue]")
        # self.stages = load_stage_modules()
        self.stages = setup_stages()
        rprint("[bold green]Pulsar stage modules loaded successfully![/bold green]")
        print_stages(self.stages)

        for stage in self.stages:
            stage.setup()

    @testcase(parameters=[
        {"num_messages": 10, "duration": 5},
        {"num_messages": 20, "duration": 10},
        {"num_messages": 30, "duration": 15},
        {"num_messages": 40, "duration": 20},
        {"num_messages": 50, "duration": 25},
    ])
    def test_send_messages(self, env, result, num_messages, duration):
        rprint(f"[bold blue]Sending {num_messages} messages...[/bold blue]")
        for stage in self.stages:
            # Skip the get_logs stage
            if stage.name == "get_logs":
                rprint(f"[bold red]Skipping stage: {stage.name}[/bold red]")
                result.log(f"Skipping stage: {stage.name}")
                continue
            rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{stage}[/yellow]")
            stage.run(params={"num_messages": num_messages, "duration": duration}, env=env, result=result)
        rprint(f"[bold blue]Messages sent successfully![/bold blue]")
        rprint(f"[bold green]Sent {num_messages} messages successfully![/bold green]")
        result.log(f"Sent {num_messages} messages successfully!")

    @testcase
    def test_run(self, env, result):
        for stage in self.stages:
            rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{stage}[/yellow]")
            stage.run(env=env, result=result)

    def teardown(self, env, result):
        for stage in self.stages:
            stage.teardown()