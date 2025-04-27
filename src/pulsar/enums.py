from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
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
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None
    duration: Optional[float] = None
    logs: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None
    subscriptions: Optional[List[str]] = None
    consumers: Optional[List[str]] = None
    producers: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    parameters: Optional[Dict[str, Any]] = None
