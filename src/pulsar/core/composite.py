# pulsar/core/composite.py
from typing import Optional, Any

from pulsar.core.models import StageResult, StageStatus
from pulsar.core.command import StageCommand


class CompositeStage(StageCommand):
    """Composite pattern for managing stage dependencies"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.substages: list[StageCommand] = []
    
    def add_substage(self, stage: StageCommand) -> None:
        """Add a substage to this composite"""
        self.substages.append(stage)
    
    def setup(self, env: Optional[dict[str, Any]] = None, result: Optional[Any] = None) -> None:
        """Set up all substages"""
        for stage in self.substages:
            stage.setup(env=env, result=result)

    def execute(self, context: dict[str, Any]) -> StageResult:
        """Execute all substages in dependency order"""
        self.status = StageStatus.RUNNING
        
        try:
            # Execute dependencies first
            for dep in self.dependencies:
                result = dep.execute(context)
                if result.status == StageStatus.FAILED:
                    self.status = StageStatus.FAILED
                    return StageResult(
                        self.name,
                        StageStatus.FAILED,
                        error=result.error
                    )
            
            # Execute substages
            results = []
            for stage in self.substages:
                result = stage.execute(context)
                results.append(result)
                if result.status == StageStatus.FAILED:
                    self.status = StageStatus.FAILED
                    return StageResult(
                        self.name,
                        StageStatus.FAILED,
                        error=result.error
                    )
            
            self.status = StageStatus.COMPLETED
            return StageResult(
                self.name,
                StageStatus.COMPLETED,
                result=results
            )
            
        except Exception as e:
            self.status = StageStatus.FAILED
            return StageResult(
                self.name,
                StageStatus.FAILED,
                error=e
            )

    def teardown(self, env: Optional[dict[str, Any]] = None, result: Optional[Any] = None) -> None:
        """Tear down all substages in reverse order"""
        try:
            # Teardown substages in reverse order
            for stage in reversed(self.substages):
                try:
                    stage.teardown(env=env, result=result)
                    if result:
                        result.log(f"Stage {stage.name} torn down successfully")
                except Exception as e:
                    if result:
                        result.log(f"Error tearing down stage {stage.name}: {str(e)}")
                    raise

            # Teardown dependencies in reverse order
            for dep in reversed(self.dependencies):
                try:
                    dep.teardown(env=env, result=result)
                    if result:
                        result.log(f"Dependency {dep.name} torn down successfully")
                except Exception as e:
                    if result:
                        result.log(f"Error tearing down dependency {dep.name}: {str(e)}")
                    raise

            # Call parent teardown -- why?
            super().teardown(env=env, result=result)
            
            if result:
                result.log(f"Workflow {self.name} torn down successfully")

        except Exception as e:
            if result:
                result.log(f"Error during workflow teardown: {str(e)}")
            raise
