# pulsar/core/builder.py

from typing import Optional, Type

from pulsar.core.command import StageCommand
from pulsar.core.composite import CompositeStage

class WorkflowBuilder:
    """Builder pattern for creating workflow DAGs"""

    def __init__(self, name: str = "main_workflow"):
        self.workflow = CompositeStage(name)
        self._stages: dict[str, StageCommand] = {}

    def _find_stage(self, name: str) -> Optional[StageCommand]:
        """Find a stage by name"""
        return self._stages.get(name)
    
    def add_stage(self, 
                  stage: StageCommand, 
                  depends_on: list[str] = None) -> 'WorkflowBuilder':
        
        """
        Add a stage to the workflow with optional dependencies
        :stage: The stage to add
        :depends_on: List of stage names this stage depends on
        :return: self for method chaining
        """
        # Store stage reference
        self._stages[stage.name] = stage

        # Add dependencies if specified
        if depends_on:
            for dep_name in depends_on:
                if dep_name not in self._stages:
                    # TODO: raise custom exception
                    raise ValueError(f"Dependency {dep_name} not found in stages")
                dependency = self._find_stage(dep_name)
                ## dependency = self._stages[dep_name]
                stage.add_dependency(dependency)

        # Add to workflow
        self.workflow.add_substage(stage)
        return self
    
    def get_stage(self, name: str) -> Optional[StageCommand]:
        """Get a stage by name"""
        return self._stages.get(name)
    
    def build(self) -> CompositeStage:
        """Build and return the workflow"""
        return self.workflow