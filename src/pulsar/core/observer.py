# pulsar/core/observer.py
from abc import ABC, abstractmethod

from pulsar.core.models import StageResult


class StageObserver(ABC):
    """Observer pattern for monitoring stage execution"""
    
    @abstractmethod
    def update(self, result: StageResult) -> None:
        """Handle stage status updates"""
        pass

class LoggingObserver(StageObserver):
    """Observer that logs stage status changes"""
    
    def __init__(self, logger):
        self.logger = logger
    
    def update(self, result: StageResult) -> None:
        self.logger.info(
            f"Stage {result.stage_name} status changed to {result.status}"
        )
        if result.error:
            self.logger.error(
                f"Stage {result.stage_name} failed: {str(result.error)}"
            )

class MetricsObserver(StageObserver):
    def __init__(self, metrics):
        self.metrics = metrics
    
    def update(self, result: StageResult):
        self.metrics.record_stage_status(
            stage_name=result.stage_name,
            status=result.status.value
        )
