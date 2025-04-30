# pulsar/core/command.py

from abc import ABC, abstractmethod
from typing import Optional, Any

from pulsar.core.models import StageResult, StageStatus
from pulsar.core.observer import StageObserver


class StageCommand(ABC):
    """Command pattern base class for stages"""
    
    def __init__(self, name: str):
        self.name = name
        self.observers: list[StageObserver] = []
        self.dependencies: list[StageCommand] = []
        self._status = StageStatus.PENDING
        
    @abstractmethod
    def execute(self, context: dict[str, Any]) -> StageResult:
        """Execute the stage command"""
        pass
    
    def teardown(self, env: Optional[dict[str, Any]] = None, result: Optional[Any] = None) -> None:
        """Base teardown method - override in subclasses if needed"""
        self.status = StageStatus.SKIPPED
        self.notify_observers(StageResult(
            self.name,
            StageStatus.SKIPPED,
            metadata={"message": "Stage teardown completed"}
        ))
    
    def add_dependency(self, dependency: 'StageCommand') -> None:
        """Add a dependency to this stage"""
        self.dependencies.append(dependency)
    
    def add_observer(self, observer: 'StageObserver') -> None:
        """Add an observer to this stage"""
        self.observers.append(observer)
    
    def notify_observers(self, result: StageResult) -> None:
        """Notify all observers of stage status change"""
        for observer in self.observers:
            observer.update(result)
            
    @property
    def status(self) -> StageStatus:
        return self._status
    
    @status.setter
    def status(self, value: StageStatus) -> None:
        self._status = value
        self.notify_observers(StageResult(self.name, value))
