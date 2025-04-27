# pulsar/di/container.py
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

from stages.factory import (
    Logger,
    Producer,
    Metrics,
    GetLogsStage,
    SendMessagesStage
)

class Container(containers.DeclarativeContainer):
    # Configure dependencies
    config = providers.Configuration()
    
    logger = providers.Singleton(Logger)
    
    producer = providers.Singleton(
        Producer,
        host=config.producer_host,
        port=config.producer_port
    )
    
    metrics = providers.Singleton(Metrics)
    
    # Stage factories
    get_logs_stage = providers.Factory(
        GetLogsStage,
        logger=logger
    )
    
    send_messages_stage = providers.Factory(
        SendMessagesStage,
        producer=producer,
        metrics=metrics
    )

# Usage with dependency injection container
@inject
def create_test_suite(
    get_logs: GetLogsStage = Provide[Container.get_logs_stage],
    send_messages: SendMessagesStage = Provide[Container.send_messages_stage]
):
    return [get_logs, send_messages]

# Configure and use the container
container = Container()
container.config.from_dict({
    "producer_host": "localhost",
    "producer_port": 9092
})

# Wire the container
container.wire(modules=[__name__])

# Create test suite with injected dependencies
stages = create_test_suite()
