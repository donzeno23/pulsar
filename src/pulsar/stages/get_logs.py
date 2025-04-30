# pulsar/stages/get_logs.py
from typing import Any, Optional

from rich import print as rprint

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
        # uses the base class setup and result.log output
        super().setup(env, result)  # Call base class setup for common logging
        
        if not cls.is_available():
            rprint(f"[bold yellow]Skipping optional stage {cls.name} - dependencies not met[/bold yellow]")
            return
        
        logger = cls.get_deps()["logger"]
        if logger:
            logger.info(f"logger.info**** Setting up {cls.name} stage")

        # Use the injected logger
        if result:
            result.log(f"testplan.result**** Setting up {cls.name} stage")

        # Add custom setup logic here
        rprint(f"[bold blue]Setting up stage:[/bold blue] [yellow]{cls.name}[/yellow]")

    @classmethod
    def run(cls, context: dict[str, Any]) -> Any:
        logger = cls.get_deps()["logger"]

        params = context.get("testcase_params", context) 
        # log_type = params.get('testcase_params', {}).get('log_type', 'application')  # default value if not found
        log_type = params.get('testcase_params', {}).get('log_type')
        logger.info(f"Running {cls.name} stage with log type: {log_type}")
        limit = params.get('testcase_params', {}).get('limit')
        logger.info(f"Retrieving {log_type} logs with a limit of {limit}")

        result = context.get("result", None)

        # Implement log retrieval logic here
        rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{cls.name}[/yellow]")

        # Log execution in test result
        if result:
            result.log(f"++++++++ Running {cls.name} stage")
            result.log(f"Retrieving log type: {log_type} logs with a limit of {limit}")

        return {"logs retrieved": []}


    def teardown(self, env: Optional[dict[str, Any]] = None, result: Optional[Any] = None) -> None:
        """
        Tear down the get_logs stage.
        :param params: Parameters for the stage.
        :param env: Environment for the stage.
        :param result: Result object for logging.
        """
        super().teardown(env, result)

        if not self.is_available():
            rprint(f"[bold yellow]Skipping optional stage {self.name} - dependencies not met[/bold yellow]")
            return

        logger = self.get_deps()["logger"]
        if logger:
            logger.info(f"******** Tearing down {self.name} stage")

        if result:
            result.log(f"Tearing down {self.name} stage")

        # Add custom teardown logic here
        rprint(f"[bold red]Tearing down {self.name} stage[/bold red]")
        result.log(f"Tearing down {self.name} stage")

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

    def _cleanup(self, env: Optional[dict[str, Any]] = None, result: Optional[Any] = None) -> None:
        """Clean up any resources used by the get_logs stage"""
        logger = self.get_deps()["logger"]
        logger.info("Cleaning up get_logs stage resources")
        # Add any specific cleanup code here
        if result:
            result.log("Cleaning up get_logs stage resources")


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