# pulsar/stages/get_logs.py
from rich import print as rprint
from typing import Any, Optional

from pulsar.stages.base_stage import BaseStage

class GetLogsStage(BaseStage):
    """Stage for retrieving and processing logs from the system."""

    name = "get_logs"
    dependencies = ["logger"]  # Required dependencies
    optional = True  # Optional stage, can be skipped if not needed
    
    metadata = {
        "description": "Retrieves and processes logs from the system",
        "version": "1.0.0",
        "author": "mdaloia",
        "tags": ["logs", "monitoring"],
        "additional_info": {
            "requires_permissions": ["read_logs"],
            "average_runtime": "2s",
            "log_retention": "30 days",
            "supported_log_types": ["application", "system", "security"],
            "output_format": ["json", "text"],
            "compression": ["gzip", "zip"],
            "encryption": ["AES", "RSA"],
        }
    }

    @classmethod
    def setup(cls, env: Optional[dict[str, Any]] = None, result: Optional[Any] = None) -> None:

        """
        Set up the get_logs stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        # Uncomment to use the base class setup and result.log output
        super().setup(env, result)  # Call base class setup for common logging
        
        if not cls.is_available():
            rprint(f"[bold yellow]Skipping optional stage {cls.name} - dependencies not met[/bold yellow]")
            return
        
        logger = cls.get_deps()["logger"]
        if logger:
            logger.info(f"**** Setting up {cls.name} stage")

        # Use the injected logger
        if result:
            result.log(f"Setting up {cls.name} stage")

        # Add custom setup logic here
        rprint(f"[bold blue]Setting up stage:[/bold blue] [yellow]{cls.name}[/yellow]")

    @classmethod
    def run(cls, 
            params: Optional[dict[str, Any]] = None, 
            env: Optional[dict[str, Any]] = None, 
            result: Optional[Any] = None) -> None:
        """
        Run the get_logs stage.
        :param params: Parameters for the stage execution.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        ## super().run(params, env, result)  # Call base class run for common logging

        if not cls.is_available():
            rprint(f"[bold yellow]Skipping optional stage {cls.name} - dependencies not met[/bold yellow]")
            return
        
        logger = cls.get_deps()["logger"]
        if logger:
            logger.info(f"******* Running {cls.name} stage")

            # Log parameters if provided
            if params:
                logger.info(f"Parameters: {params}")

        # Add your custom log retrieval logic here
        rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{cls.name}[/yellow]")

        # Example of using parameters
        log_type = params.get('log_type', 'application') if params else 'application'
        limit = params.get('limit', 100) if params else 100
        logger.info(f"Retrieving {log_type} logs with a limit of {limit}")

        # Log execution in test result
        if result:
            result.log(f"++++++++ Running {cls.name} stage")
            result.log(f"Retrieving log type: {log_type} logs with a limit of {limit}")

    @classmethod
    def teardown(cls, 
                params: Optional[dict[str, Any]] = None, 
                env: Optional[dict[str, Any]] = None, 
                result: Optional[Any] = None) -> None:
        """
        Tear down the get_logs stage.
        :param params: Parameters for the stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        # super().teardown(params, env, result)

        if not cls.is_available():
            rprint(f"[bold yellow]Skipping optional stage {cls.name} - dependencies not met[/bold yellow]")
            return

        logger = cls.get_deps()["logger"]
        if logger:
            logger.info(f"******** Tearing down {cls.name} stage")

        if result:
            result.log(f"Tearing down {cls.name} stage")

        # Add custom teardown logic here
        rprint(f"[bold red]Tearing down {cls.name} stage[/bold red]")
        result.log(f"Tearing down {cls.name} stage")

    @classmethod
    def is_available(cls) -> bool:
        """
        Check if the stage is available based on its dependencies.
        :return: True if the stage is available, False otherwise.
        """
        # Check if all dependencies are met
        for dep in cls.dependencies:
            if dep not in cls.get_deps():
                return False
        return True
        
        # Check if logger dependency is available
        # return "logger" in cls.get_deps()


# class GetLogsStage(BaseStage):
#     name = "get_logs"
#     dependencies = []  # No dependencies for this stage

#     @classmethod
#     def run(cls, params=None, env=None, result=None):
#         print(f"Running the {cls.name} stage.")
#         rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{cls.name}[/yellow]")
#         # Add custom get_logs logic here

# Create module-level functions that use the class methods
def init_dependencies(**dependencies: Any) -> None:
    """Initialize the stage's dependencies."""
    GetLogsStage.set_dependencies(**dependencies)

# Export commonly used attributes and methods
setup = GetLogsStage.setup
run = GetLogsStage.run
teardown = GetLogsStage.teardown
name = GetLogsStage.name
metadata = GetLogsStage.get_metadata
is_available = GetLogsStage.is_available