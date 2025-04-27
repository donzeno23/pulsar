# pulsar/stages/base_stage.py
from typing import Any, Optional
from abc import ABC
from rich import print as rprint

from pulsar.exceptions import PulsarStageDependencyError

from testplan.common.entity.base import Runnable
from testplan.testing.result import Result


class BaseStage(ABC):
    """Base class template for all Pulsar stages"""
    
    name: str = "base_stage"  # Override this in child classes
    dependencies: list[str] = []  # Override this in child classes if needed
    _deps: dict[str, Any] = {}  # Class level storage for dependencies

    @classmethod
    def set_dependencies(cls, **dependencies: Any) -> None:
        """
        Set dependencies for the stage.
        
        Args:
            **dependencies: Dependencies to inject into the stage
        """
        cls._deps = dependencies
        cls.validate_dependencies()

    @classmethod
    def validate_dependencies(cls) -> None:
        """Validate that all required dependencies are present."""
        missing_deps = [dep for dep in cls.dependencies if dep not in cls._deps]
        if missing_deps:
            raise PulsarStageDependencyError(
                stage_name=cls.name,
                dependency=missing_deps,
                message=f"Missing required dependencies for {cls.name}: {missing_deps}"
            )

    @classmethod
    def get_deps(cls) -> dict[str, Any]:
        """
        Get the stage's dependencies.
        
        Returns:
            Dict[str, Any]: Dictionary of dependencies
        """
        return cls._deps

    @classmethod
    def setup(cls, env: Optional[Runnable] = None, result: Optional[Result] = None):
        """Setup function to initialize the stage."""
        print(f"Setting up the {cls.name} stage.")
        rprint(f"[bold green]{cls.name} stage initialized.[/bold green]")
        if result:
            result.log(f"Setting up the {cls.name} stage.")
            result.log(f"{cls.name} stage initialized.")

    @classmethod
    def run(cls, params: Optional[dict] = None, env: Optional[Runnable] = None, 
            result: Optional[Result] = None):
        """
        Run function to execute the stage.
        
        Args:
            params: Parameters for the stage
            env: Environment for the stage
            result: Result object to store the results
        """
        print(f"Running the {cls.name} stage.")
        rprint(f"[bold green] Using these parameters: '{params}' for the stage: '{cls.name}'.[/bold green]")
        
        if result:
            result.log(f"Running the {cls.name} stage.")
            result.log(f"Using these parameters: '{params}' for the stage: '{cls.name}'.")

    @classmethod
    def teardown(cls):
        """Teardown function to clean up after the stage."""
        print(f"Tearing down the {cls.name} stage.")
        rprint(f"[bold red]{cls.name} stage has been torn down![/bold red]")
