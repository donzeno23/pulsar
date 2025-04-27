from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union
from typing_extensions import Literal


class PulsarStageType(Enum):
    """
    Enum for different types of Pulsar stages.
    """
    SEND_MESSAGES = "send_messages"
    GET_LOGS = "get_logs"
    GET_METRICS = "get_metrics"
    GET_SUBSCRIPTIONS = "get_subscriptions"
    GET_CONSUMERS = "get_consumers"
    GET_PRODUCERS = "get_producers"
    GET_TOPICS = "get_topics"

class PulsarStageStatus(Enum):
    """
    Enum for different statuses of Pulsar stages.
    """
    SUCCESS = "success"
    FAILURE = "failure"
    RUNNING = "running"
    NOT_STARTED = "not_started"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"
    ABORTED = "aborted"
    CANCELLED = "cancelled"
    NOT_EXECUTED = "not_executed"
    ERROR = "error"
    UNKNOWN = "unknown"

@dataclass
class PulsarStageResult:
    """
    Dataclass for Pulsar stage results.
    """
    stage: PulsarStageType
    status: PulsarStageStatus
    result: Any
    error: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    timestamp: Optional[str] = None
    duration: Optional[float] = None
    logs: Optional[list[str]] = None
    metrics: Optional[dict[str, Any]] = None
    subscriptions: Optional[list[str]] = None
    consumers: Optional[list[str]] = None
    producers: Optional[list[str]] = None
    topics: Optional[list[str]] = None
    parameters: Optional[dict[str, Any]] = None

@dataclass
class StageMetadata:
    """
    Dataclass for stage metadata.
    """
    name: str
    module: str
    description: str
    type: PulsarStageType
    status: PulsarStageStatus
    dependencies: list[str]
    optional: bool = False
    parameters: Optional[dict[str, Any]] = None
    version: str = "0.0.0"
    author: str = "Unknown"
    additional_info: Optional[dict[str, Any]] = None
    tags: Optional[list[str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None