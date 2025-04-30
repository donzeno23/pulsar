# pulsar/stages/base_stage.py
from typing import Any, Optional
from abc import ABC, abstractmethod
from rich import print as rprint

from pulsar.core.exceptions import PulsarStageDependencyError
from pulsar.core.models import StageMetadata, StageStatus, StageResult
from pulsar.core.exceptions import PulsarStageExecutionFailureError
from pulsar.core.command import StageCommand

from testplan.common.entity.base import Runnable
from testplan.testing.multitest.base import RuntimeEnvironment
from testplan.testing.result import Result


class BaseStage(StageCommand):
    """Base class for all Pulsar Stages incorporating command pattern"""
    
    name: str = "base_stage" # Override this in child class
    optional: bool = False
    dependencies: list[str] = []
    metadata: dict[str, Any] = {}
    _deps: dict[str, Any] = {}

    def __init__(self):
        # Pass the class-level name to the parent class
        super().__init__(self.__class__.name)
        self._deps: dict[str, Any] = {}

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

    @classmethod
    def setup(cls, env: Optional[Runnable] = None, result: Optional[Result] = None):
        """Setup function to initialize the stage."""
        if not cls.is_available():
            rprint(f"[bold yellow]Skipping setup for optional stage {cls.name} - dependencies not met[/bold yellow]")
            return
        
        print(f"****base-stage**** Setting up the {cls.name} stage.")
        rprint(f"[bold green]****base-stage**** {cls.name} stage initialized.[/bold green]")
        if result:
            result.log(f"****base-stage**** Setting up the {cls.name} stage.")
            result.log(f"****base-stage**** {cls.name} stage initialized.")

    def execute(self, context: dict[str, Any]) -> StageResult:
        """Execute the stage with proper lifecycle"""
        self.status = StageStatus.RUNNING

        try:
            env = context.get("env", None)
            result = context.get("result", None)

            self.setup(env, result)
            # Run stage logic
            run_result = self.run(context)
            self.teardown(env, result)
            self.status = StageStatus.COMPLETED

            return StageResult(
                self.name,
                StageStatus.COMPLETED,
                result=run_result
            )
        except PulsarStageExecutionFailureError as e:
            self.status = StageStatus.FAILED
            return StageResult(
                self.name,
                StageStatus.FAILED,
                error=e
            )

    @abstractmethod
    def run(self, context: dict[str, Any]) -> Any:
        """ Implement stage-specific logic """
        if not self.is_available():
            rprint(f"[bold yellow]Skipping optional stage {self.name} - dependencies not met[/bold yellow]")
            return
        
        params = context.get("testcase_params", context) 
        env = context.get("env", {})
        result = context.get("result", None)
        
        print(f"Running the {self.name} stage.")
        rprint(f"[bold green] Using these parameters: '{params}' for the stage: '{self.name}'.[/bold green]")
        
        if result:
            result.log(f"Running the {self.name} stage.")
            result.log(f"Using these parameters: '{params}' for the stage: '{self.name}'.")


    def teardown(self, env: Optional[dict[str, Any]] = None, result: Optional[Any] = None) -> None:
        """Tear down the stage and clean up resources"""

        if not isinstance(result, Result):
          
            print(type(result))
            raise PulsarStageExecutionFailureError(
                stage_name=self.name,
                error_message=f"Result object is not of type Result"
            )
        if not isinstance(env, RuntimeEnvironment): # Runnable):
            print(type(env))
            raise PulsarStageExecutionFailureError(
                stage_name=self.name,
                error_message=f"Environment object is not of type Runnable"
            )

        try:
            # Perform stage-specific cleanup
            self._cleanup(env, result)
            
            # Call parent teardown -- why??
            super().teardown(env=env, result=result)
            
            if result:
                result.log(f"Stage {self.name} torn down successfully")
                
        except Exception as e:
            if result:
                result.log(f"Error tearing down stage {self.name}: {str(e)}")
            if not self.optional:
                raise

    def _cleanup(self, env: Optional[dict[str, Any]] = None, result: Optional[Any] = None) -> None:
        """Override this method in subclasses to perform specific cleanup"""
        pass