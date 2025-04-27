# pulsar/stages/factory.py
from typing import Type, Any

from rich import print as rprint

from pulsar.stages.base_stage import BaseStage
from pulsar.stages.get_logs import GetLogsStage
from pulsar.stages.send_messages import SendMessagesStage
from pulsar.exceptions import PulsarStageDependencyError
from pulsar.core.dependencies import Logger, Producer, Metrics

class StageFactory:
    """Factory class for creating and managing stages with dependency injection. """

    def __init__(self):
        """Initialize the StageFactory with empty metadata and dependencies."""

        self._metadata = {}
        self._dependencies = {}
        self._stage_classes = {}

    def register_dependency(self, name: str, dependency: Any):
        """Register a dependency that can be injected into stages.
        
        :param name: Name of the dependency.
        :param dependency: The dependency instance to register.
        """
        self._dependencies[name] = dependency

    def register_stage(self, stage_class: Type[BaseStage]):
        """Register a stage class that can be instantiated.
        
        :param stage_class: The stage class to register.
        """
        self._stage_classes[stage_class.name] = stage_class
        self._metadata[stage_class.name] = stage_class.get_metadata()

    def get_stage_metadata(self, stage_name: str) -> dict[str, Any]:
        """Get metadata for a registered stage.
        
        :param stage_name: Name of the stage.
        :return: Metadata dictionary for the stage.
        :raises ValueError: If the stage is not registered.
        """
        if stage_name not in self._metadata:
            # TODO: add a custom StageCreationError
            raise ValueError(f"Unknown stage: {stage_name}")
        return self._metadata[stage_name]

    def create_stage(self, stage_name: str) -> BaseStage:
        """Create a stage instance with its dependencies injected.
        
        :param stage_name: Name of the stage to create.
        :return: An instance of the requested stage.
        :raises ValueError: If the stage is not registered or dependencies are missing.
        """
        if stage_name not in self._stage_classes:
            # TODO: add a custom StageCreationError
            raise ValueError(f"Unknown stage: {stage_name}")

        stage_class = self._stage_classes[stage_name]

        # Get required dependencies for the stage
        required_deps = {
            dep: self._dependencies[dep]
            for dep in stage_class.dependencies
            if dep in self._dependencies
        }

        # Set dependencies on the stage class
        stage_class.set_dependencies(**required_deps)
        
        if not stage_class.optional:
            missing_deps = [dep for dep in stage_class.dependencies if dep not in required_deps]
            if missing_deps:
                raise PulsarStageDependencyError(
                    stage_name=stage_name,
                    dependency=missing_deps,
                    message=f"Missing required dependencies for {stage_name}: {missing_deps}"
                )
        
        # return stage_class(**required_deps)
        return stage_class


def setup_stages() -> list[Type[BaseStage]]:
    """
    Setup the stages by creating a factory and registering dependencies.
    :return: List of instantiated stages with dependencies injected.
    :rtype: list[Type[BaseStage]]
    :raises ValueError: If a stage is not registered or a dependency is missing.
    """
    # Create factory and register dependencies
    factory = StageFactory()
    
    # Register common dependencies
    factory.register_dependency("logger", Logger())
    factory.register_dependency("producer", Producer())
    factory.register_dependency("metrics", Metrics())

    # Register stages
    factory.register_stage(GetLogsStage)
    factory.register_stage(SendMessagesStage)
    
    available_stages = []

    # Create stages and check availability
    for stage_name, stage_class in factory._stage_classes.items():
        try:
            stage = factory.create_stage(stage_name)

            if stage.is_available():
                available_stages.append(stage)
                rprint(f"[bold green]Stage {stage_name} is available and initialized successfully![/bold green]")
            else:
              if stage.optional:
                rprint(f"[bold yellow]Stage {stage_name} is optional and not available.[/bold yellow]")
              else:
                rprint(f"[bold red]Stage {stage_name} is not available and is required![/bold red]")
                rprint(f"[yellow]Optional stage {stage_name} skipped - dependencies not met[/yellow]")
                raise PulsarStageDependencyError(
                    stage_name=stage_name,
                    dependency=stage.dependencies,
                    # message=f"Stage {stage_name} is not available."
                    message=f"Required stage {stage_name} missing dependencies"
                )
        except Exception as e:
            if not stage_class.optional:
                raise PulsarStageDependencyError(
                    stage_name=stage_name,
                    dependency=stage_class.dependencies,
                    message=f"Failed to initialize required stage {stage_name}: {str(e)}"
                )
            rprint(f"[bold red]Failed to create stage {stage_name}: {str(e)}[/bold red]")
            rprint(f"[yellow]Optional stage {stage_name} skipped - {str(e)}[/yellow]")
    
    return available_stages


def get_available_stages() -> list[Type[BaseStage]]:
    """
    Get a list of available stages.
    
    :return: List of available stage classes.
    :rtype: list[Type[BaseStage]]
    """
    factory = StageFactory()
    return list(factory._stage_classes.values())
    # return setup_stages()

def get_stage_metadata(stage_name: str) -> dict[str, Any]:
    """
    Get metadata for a specific stage.

    :param stage_name: Name of the stage.
    :return: Metadata dictionary for the stage.
    :rtype: dict[str, Any]
    :raises ValueError: If the stage is not registered.
    """
    factory = StageFactory()
    return factory.get_stage_metadata(stage_name)

def create_stage(stage_name: str) -> BaseStage:
    """
    Create a stage instance with its dependencies injected.

    :param stage_name: Name of the stage to create.
    :return: An instance of the requested stage.
    :rtype: BaseStage
    :raises ValueError: If the stage is not registered or dependencies are missing.
    """
    factory = StageFactory()
    return factory.create_stage(stage_name)