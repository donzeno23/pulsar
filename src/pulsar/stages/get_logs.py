# pulsar/stages/get_logs.py
from rich import print as rprint

from pulsar.stages.base_stage import BaseStage

class GetLogsStage(BaseStage):
    name = "get_logs"
    dependencies = ["logger"]  # Example dependency

    @classmethod
    def setup(cls, env=None, result=None):

        """
        Set up the get_logs stage.
        :param params: Parameters for the stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        super().setup(env, result)  # Call base class setup for common logging
        logger = cls.get_deps()["logger"]
        logger.info(f"***** Setting up {cls.name} stage")
        # Use the injected logger
        # if result:
        #     result.log(f"Setting up {cls.name} stage")
        # Add custom setup logic here

    @classmethod
    def run(cls, params=None, env=None, result=None):
        """
        Run the get_logs stage.
        :param params: Parameters for the stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        super().run(params, env, result)  # Call base class run for common logging
        logger = cls.get_deps()["logger"]
        logger.info(f"******* Running {cls.name} stage")
        # Use the injected logger
        # if result:
        #     result.log(f"Running {cls.name} stage")

        # Add your custom log retrieval logic here
        rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{cls.name}[/yellow]")

    @classmethod
    def teardown(cls, params=None, env=None, result=None):
        """
        Tear down the get_logs stage.
        :param params: Parameters for the stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        # super().teardown(params, env, result)
        logger = cls.get_deps()["logger"]
        logger.info(f"Tearing down {cls.name} stage")
        # Use the injected logger
        if result:
            result.log(f"Tearing down {cls.name} stage")
        # Add custom teardown logic here


# class GetLogsStage(BaseStage):
#     name = "get_logs"
#     dependencies = []  # No dependencies for this stage

#     @classmethod
#     def run(cls, params=None, env=None, result=None):
#         print(f"Running the {cls.name} stage.")
#         rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{cls.name}[/yellow]")
#         # Add custom get_logs logic here

# Create module-level functions that use the class methods
setup = GetLogsStage.setup
run = GetLogsStage.run
teardown = GetLogsStage.teardown
name = GetLogsStage.name
