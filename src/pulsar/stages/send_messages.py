# pulsar/stages/send_messages.py
from rich import print as rprint

from pulsar.stages.base_stage import BaseStage
from pulsar.exceptions import PulsarStageInvalidParameterError

class SendMessagesStage(BaseStage):
    name = "send_messages"
    dependencies = ["producer", "metrics", "logger"]  # Example dependencies

    @classmethod
    def setup(cls, params=None, env=None, result=None):
        """
        Set up the send_messages stage.
        :param params: Parameters for the stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        # TODO: Uncomment to use the base class setup
        # super().setup(params, env, result)
        logger = cls.get_deps()["logger"]
        logger.info(f"Setting up {cls.name} stage")
        # Use the injected logger
        logger.info(f"******** Setting up {cls.name} stage")

        # TODO: Comment out if using the base class setup
        # Add custom setup logic here
        if result:
            result.log(f"========= Setting up {cls.name} stage =========")
        # Add custom setup logic here

    @classmethod
    def run(cls, params=None, env=None, result=None):
        """
        Run the send_messages stage.
        :param params: Parameters for the stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        super().run(params, env, result)  # Call base class run for common logging

        if not params:
            rprint("[bold red]No parameters provided for the stage.[/bold red]")
            raise PulsarStageInvalidParameterError(stage_name=cls.name, parameter=params, message="No params were provided for the stage.")
        
        if "num_messages" not in params:
            rprint("[bold red]No message provided for the stage.[/bold red]")
            # return False
            raise PulsarStageInvalidParameterError(stage_name=cls.name, parameter=params, message="No message param provided for the stage.")
        
        if "duration" not in params:
            rprint("[bold red]No duration provided for the stage.[/bold red]")
            raise PulsarStageInvalidParameterError(stage_name=cls.name, parameter=params, message="No duration param provided for the stage.")

        producer = cls.get_deps()["producer"]
        metrics = cls.get_deps()["metrics"]
        # Use the injected dependencies
        producer.send_message(params["num_messages"])
        metrics.record_send()

    @classmethod
    def teardown(cls, params=None, env=None, result=None):
        """
        Tear down the send_messages stage.
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


# class SendMessagesStage(BaseStage):
#     name = "send_messages"
#     dependencies = ["get_logs"]

#     @classmethod
#     def run(cls, params=None, env=None, result=None):
#         super().run(params, env, result)  # Call base class run for common logging

#         if not params:
#             rprint("[bold red]No parameters provided for the stage.[/bold red]")
#             if result:
#                 result.log(f"No parameters provided for the stage: '{cls.name}'")
#             raise PulsarStageInvalidParameterError(
#                 stage_name=cls.name, 
#                 parameter=params,
#                 message="No parameters provided for the stage. Required: 'num_messages', 'duration', 'topic'."
#             )
        
#         # Add your parameter validation
#         required_params = ['num_messages', 'duration', 'topic']
#         for param in required_params:
#             if param not in params:
#                 rprint(f"[bold red]No {param} provided for the stage.[/bold red]")
#                 raise PulsarStageInvalidParameterError(
#                     stage_name=cls.name,
#                     parameter=params,
#                     message=f"Missing {param} parameter. Required: 'num_messages', 'duration', 'topic'."
#                 )

#         # Add custom send_messages logic here
#         rprint("[bold blue]Pulsar stage is running![/bold blue]")

# Create module-level functions that use the class methods
# def init_dependencies(**dependencies):
#     """Initialize the stage's dependencies."""
#     GetLogsStage.set_dependencies(**dependencies)

setup = SendMessagesStage.setup
run = SendMessagesStage.run
teardown = SendMessagesStage.teardown
name = SendMessagesStage.name
