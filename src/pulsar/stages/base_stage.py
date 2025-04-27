# pulsar/stages/base_stage.py
from typing import Any, Optional
from abc import ABC
from rich import print as rprint

from pulsar.exceptions import PulsarStageDependencyError
from pulsar.enums import StageMetadata

from testplan.common.entity.base import Runnable
from testplan.testing.result import Result


class BaseStage(ABC):
    """Base class template for all Pulsar stages"""
    
    name: str = "base_stage"  # Override this in child classes
    optional: bool = False  # Override this in child classes if needed
    dependencies: list[str] = []  # Override this in child classes if needed
    metadata: dict[str, Any] = {}  # Override this in child classes if needed
    _deps: dict[str, Any] = {}  # Class level storage for dependencies

    @classmethod
    def set_dependencies(cls, **dependencies: Any) -> None:
        """
        Set dependencies for the stage.
        
        Args:
            **dependencies: Dependencies to inject into the stage
        """
        cls._deps = dependencies
        if not cls.optional: # Only validate if the stage is not optional
          cls.validate_dependencies()

    @classmethod
    def validate_dependencies(cls) -> None:
        """Validate that all required dependencies are present."""
        if not cls.optional: # Only validate if stage is not optional
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
    def get_metadata(cls) -> StageMetadata:
        """
        Get the stage's metadata.
        
        Returns:
                StageMetadata: Metadata object containing stage information
        """
        return StageMetadata(
            name=cls.name,
            module=cls.__module__,
            dependencies=cls.dependencies,
            optional=cls.optional,
            type=cls.metadata.get('type'),
            status=cls.metadata.get('status'),
            parameters=cls.metadata.get('parameters'),
            description=cls.metadata.get('description'),
            version=cls.metadata.get('version'),
            author=cls.metadata.get('author'),
            tags=cls.metadata.get('tags'),
            additional_info=cls.metadata.get('additional_info')
        )
    
    @classmethod
    def is_available(cls) -> bool:
        """
        Check if the stage is available for execution.
        
        Returns:
            bool: True if the stage is available, False otherwise
        """
        if cls.optional:
            all(dep in cls._deps for dep in cls.dependencies)
        return True
        # return cls.optional or all(dep in cls._deps for dep in cls.dependencies)

    @classmethod
    def setup(cls, env: Optional[Runnable] = None, result: Optional[Result] = None):
        """Setup function to initialize the stage."""
        if not cls.is_available():
            rprint(f"[bold yellow]Skipping setup for optional stage {cls.name} - dependencies not met[/bold yellow]")
            return
        
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
        if not cls.is_available():
            rprint(f"[bold yellow]Skipping optional stage {cls.name} - dependencies not met[/bold yellow]")
            return
        
        print(f"Running the {cls.name} stage.")
        rprint(f"[bold green] Using these parameters: '{params}' for the stage: '{cls.name}'.[/bold green]")
        
        if result:
            result.log(f"Running the {cls.name} stage.")
            result.log(f"Using these parameters: '{params}' for the stage: '{cls.name}'.")

    @classmethod
    def teardown(cls):
        """Teardown function to clean up after the stage."""
        if not cls.is_available():
            rprint(f"[bold yellow]Skipping teardown for optional stage {cls.name} - dependencies not met[/bold yellow]")
            return
        
        print(f"Tearing down the {cls.name} stage.")
        rprint(f"[bold red]{cls.name} stage has been torn down![/bold red]")
