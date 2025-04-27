# pulsar/stages/send_messages.py
from typing import Any, Optional

from rich import print as rprint

from pulsar.stages.base_stage import BaseStage
from pulsar.core.dependencies import Producer, Metrics, Logger
from pulsar.exceptions import PulsarStageInvalidParameterError

class SendMessagesStage(BaseStage):
    name = "send_messages"
    dependencies = ["producer", "metrics", "logger"]  # Required dependencies
    optional = False  # This stage is required

    _producer_connected = False  # Flag to check if producer is connected

    metadata = {
        "name": name,
        "description": "Stage to send messages to a Pulsar topic.",
        "verion": "1.0",
        "author": "Pulsar Team",
        "tags": ["producer", "messages", "performance"],
        "dependencies": dependencies,
        "optional": optional,
        "parameters": {
            "num_messages": {
                "type": int,
                "description": "Number of messages to send."
            },
            "duration": {
                "type": int,
                "description": "Duration for sending messages."
            }
        },
        "additional_info": {
            "requires_permissions": ["write_messages"],
            "average_runtime": "varies by message count",
            "supported_message_types": ["string", "json", "bytes"]
        }
    }

    @classmethod
    def setup(cls, env: Optional[dict[str, Any]] = None, result: Optional[Any] = None) -> None:
        """
        Set up the send_messages stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        # TODO: Uncomment to use the base class setup
        # super().setup(params, env, result)

        if not cls.is_available():
            rprint(f"[bold red]Cannot setup {cls.name} - dependencies not met[/bold red]")
            result.log(f"Cannot setup {cls.name} - dependencies not met")
            raise RuntimeError(f"Required stage {cls.name} missing dependencies")
        
        logger = cls.get_deps()["logger"]
        producer = cls.get_deps()["producer"]

        if logger:
            logger.info(f"******** Setting up {cls.name} stage")

        # TODO: Comment out if using the base class setup
        if result:
            result.log(f"========= Setting up {cls.name} stage =========")

        # Add custom setup logic here
        try:
            rprint(f"[bold blue]Setting up stage:[/bold blue] [yellow]{cls.name}[/yellow]")
            result.log(f"Connecting to producer for stage: {cls.name}")

            # Connect the producer if not already connected
            if not cls._producer_connected:
                logger.info("Connecting producer...")
                producer.connect()
                cls._producer_connected = True
                logger.info("Producer connected successfully")
            
            if result:
                result.log(f"Setting up {cls.name} stage - producer connected")
                
            rprint(f"[bold green]Setting up {cls.name} stage - producer connected[/bold green]")
            
        except Exception as e:
            error_msg = f"Failed to connect producer in {cls.name}: {str(e)}"
            logger.error(error_msg)
            if result:
                result.log(error_msg)
            raise RuntimeError(error_msg)

    @classmethod
    def run(cls, 
            params: Optional[dict[str, Any]] = None, 
            env: Optional[dict[str, Any]] = None, 
            result: Optional[Any] = None) -> None:
        """
        Run the send_messages stage.

        :param params: Parameters for the stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        super().run(params, env, result)  # Call base class run for common logging

        if not cls.is_available():
            # TODO: add custom exception
            raise RuntimeError(f"Required stage {cls.name} missing dependencies")

        if not cls._producer_connected:
            # TODO: add custom exception
            raise RuntimeError(f"Producer not connected in {cls.name} stage")

        logger = cls.get_deps()["logger"]
        producer = cls.get_deps()["producer"]
        metrics = cls.get_deps()["metrics"]

        if logger:
            logger.info(f"Running {cls.name} stage")

        # Validate parameters
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

        num_messages = params['num_messages']
        logger.info(f"Sending {num_messages} messages")

        # Use the injected dependencies
        try:
            for i in range(num_messages):
                message = f"Test message {i}"
                producer.send_message(message)
                metrics.record_send(value=1.0, tags={"stage": cls.name})
                
            if result:
                result.log(f"Successfully sent {num_messages} messages")
                
            rprint(f"[bold green]Successfully sent {num_messages} messages[/bold green]")
            
        except Exception as e:
            error_msg = f"Error sending messages in {cls.name}: {str(e)}"
            logger.error(error_msg)
            if result:
                result.log(error_msg)
            raise RuntimeError(error_msg)

    @classmethod
    def teardown(cls, 
                params: Optional[dict[str, Any]] = None, 
                env: Optional[dict[str, Any]] = None, 
                result: Optional[Any] = None) -> None:
        """
        Tear down the send_messages stage.
        :param params: Parameters for the stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        # super().teardown(params, env, result)

        if not cls.is_available():
            return
        
        logger = cls.get_deps()["logger"]
        producer = cls.get_deps()["producer"]
        
        if logger:
            logger.info(f"Tearing down {cls.name} stage")

        # Use the injected logger
        if result:
            result.log(f"Tearing down {cls.name} stage")

        # Add custom teardown logic here
        try:
            if cls._producer_connected:
                producer.disconnect()
                cls._producer_connected = False
                logger.info("Producer disconnected successfully")
            
            if result:
                result.log(f"Tearing down {cls.name} stage - producer disconnected")
                
            rprint(f"[bold red]Tearing down {cls.name} stage - producer disconnected[/bold red]")
            
        except Exception as e:
            error_msg = f"Error disconnecting producer in {cls.name}: {str(e)}"
            logger.error(error_msg)
            if result:
                result.log(error_msg)
            if not cls.optional:
                raise RuntimeError(error_msg)


# Create module-level functions that use the class methods
def init_dependencies(**dependencies):
    """Initialize the stage's dependencies."""
    SendMessagesStage.set_dependencies(**dependencies)

setup = SendMessagesStage.setup
run = SendMessagesStage.run
teardown = SendMessagesStage.teardown
name = SendMessagesStage.name
metadata = SendMessagesStage.get_metadata
is_available = SendMessagesStage.is_available