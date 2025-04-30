# pulsar/utils/helpers.py
from typing import Type, Any
from rich import print as rprint
from pulsar.stages.base_stage import BaseStage


def create_context(env: dict[str, Any], result: Any, **params) -> dict[str, Any]:
    """Helper to create consistent context dictionary"""
    return {
        "testcase_params": params,
        "env": env,
        "result": result
    }

def print_stages(stages: list[Type[BaseStage]]) -> None:
    """
    Pretty prints the list of stages to be executed.
    
    Args:
        stages: List of stage classes to print information about
    """
    rprint("[bold blue]Stages to be executed:[/bold blue]")
    for i, stage in enumerate(stages, 1):
        metadata = stage.get_metadata()
        rprint(f"[green]{i}.[/green] [yellow]{metadata.name}[/yellow]")
        rprint(f"    Optional: {metadata.optional}")
        rprint(f"    Dependencies: {metadata.dependencies}")
        if metadata.description:
            rprint(f"    Description: {metadata.description}")

def init_stage_dependencies(factory, stage_class: Type[BaseStage], **dependencies) -> None:
    """
    Helper method to initialize stage dependencies.
    
    Args:
        factory: StageFactory instance
        stage_class: Stage class to initialize dependencies for
        **dependencies: Dependencies to register and initialize
    """
    # Register with factory
    for name, dep in dependencies.items():
        factory.register_dependency(name, dep)
    
    # Initialize stage dependencies
    stage_class.set_dependencies(**dependencies)

def setup_test_dependencies(factory):
    """
    Set up mock dependencies for testing.
    
    Args:
        factory: StageFactory instance to register dependencies with
        
    Returns:
        dict: Dictionary of created mock dependencies
    """
    from pulsar.tests.mock_dependencies import MockLogger, MockProducer, MockMetrics
    
    # Create mock dependencies
    deps = {
        "logger": MockLogger(),
        "producer": MockProducer(),
        "metrics": MockMetrics()
    }
    
    # Register with factory
    for name, dep in deps.items():
        factory.register_dependency(name, dep)
    
    return deps


def validate_stage_configuration(stage_class: Type[BaseStage]) -> bool:
    """
    Validate a stage's configuration.
    
    Args:
        stage_class: Stage class to validate
        
    Returns:
        bool: True if configuration is valid
    """
    # Add validation logic
    pass

def get_available_stages(factory) -> list[str]:
    """
    Get list of available stage names.
    
    Args:
        factory: StageFactory instance
        
    Returns:
        List[str]: Names of available stages
    """
    return list(factory._stage_classes.keys())

def format_stage_results(stage_results: dict) -> str:
    """
    Format stage results for display.
    
    Args:
        stage_results: Dictionary of stage results
        
    Returns:
        str: Formatted results string
    """
    # Add formatting logic
    pass