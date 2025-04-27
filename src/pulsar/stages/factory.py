# pulsar/stages/factory.py
from typing import Type, Any
from pulsar.stages.base_stage import BaseStage
from pulsar.stages.get_logs import GetLogsStage
from .send_messages import SendMessagesStage

# Dependency classes
class Logger:
    def info(self, msg): print(msg)

class Producer:
    def send_message(self, msg): print(f"Sending: {msg}")

class Metrics:
    def record_send(self): print("Recording metric")


class StageFactory:
    def __init__(self):
        self._dependencies = {}
        self._stage_classes = {}

    def register_dependency(self, name: str, dependency: Any):
        """Register a dependency that can be injected into stages."""
        self._dependencies[name] = dependency

    def register_stage(self, stage_class: Type[BaseStage]):
        """Register a stage class that can be instantiated."""
        self._stage_classes[stage_class.name] = stage_class

    def create_stage(self, stage_name: str) -> BaseStage:
        """Create a stage instance with its dependencies injected."""
        if stage_name not in self._stage_classes:
            raise ValueError(f"Unknown stage: {stage_name}")

        stage_class = self._stage_classes[stage_name]
        required_deps = {
            dep: self._dependencies[dep]
            for dep in stage_class.dependencies
            if dep in self._dependencies
        }
        
        return stage_class(**required_deps)


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
    
    # Create stages with dependencies injected
    # get_logs_stage = factory.create_stage("get_logs")
    # send_messages_stage = factory.create_stage("send_messages")
    
    # return [get_logs_stage, send_messages_stage]

    # Create dependencies
    logger = Logger()
    producer = Producer()
    metrics = Metrics()
    
    # Set up each stage with its dependencies
    GetLogsStage.set_dependencies(logger=logger)
    SendMessagesStage.set_dependencies(
        producer=producer,
        metrics=metrics,
        logger=logger
    )
    
    # Return list of stage classes
    return [GetLogsStage, SendMessagesStage]