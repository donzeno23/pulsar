# pulsar/core/dependencies.py
from abc import ABC, abstractmethod
from typing import Any, Dict
import logging


class BaseDependency(ABC):
    """Base class for all dependencies"""
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the dependency is available"""
        pass

class Logger(BaseDependency):
    """Logging dependency for stages"""
    
    def __init__(self, log_level=logging.INFO):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(log_level)
        
        # Add console handler if none exists
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def info(self, msg: str) -> None:
        """Log info message"""
        self._logger.info(msg)

    def error(self, msg: str) -> None:
        """Log error message"""
        self._logger.error(msg)

    def debug(self, msg: str) -> None:
        """Log debug message"""
        self._logger.debug(msg)

    def warning(self, msg: str) -> None:
        """Log warning message"""
        self._logger.warning(msg)

    def is_available(self) -> bool:
        """Check if logger is available"""
        return True

class Producer(BaseDependency):
    """Message producer dependency"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._connected = False

    def connect(self) -> None:
        """Connect to the message broker"""
        # Add your connection logic here
        self._connected = True

    def disconnect(self) -> None:
        """Disconnect from the message broker"""
        # Add your disconnection logic here
        self._connected = False

    def send_message(self, msg: str) -> None:
        """Send a message"""
        if not self._connected:
            raise RuntimeError("Producer not connected")
        print(f"Sending: {msg}")

    def is_available(self) -> bool:
        """Check if producer is available"""
        ## return self._connected
        # Simulate availability for testing purposes
        return True

class Metrics(BaseDependency):
    """Metrics collection dependency"""
    
    def __init__(self, namespace: str = "pulsar"):
        self.namespace = namespace
        self._metrics = {}

    def record_send(self, value: float = 1.0, tags: Dict[str, str] = None) -> None:
        """Record a send metric"""
        metric_name = f"{self.namespace}.messages.sent"
        self._metrics[metric_name] = self._metrics.get(metric_name, 0) + value
        print(f"Recording metric: {metric_name} = {self._metrics[metric_name]}")

    def record_latency(self, value: float, operation: str) -> None:
        """Record a latency metric"""
        metric_name = f"{self.namespace}.latency.{operation}"
        self._metrics[metric_name] = value
        print(f"Recording latency: {metric_name} = {value}ms")

    def get_metric(self, name: str) -> float:
        """Get a metric value"""
        return self._metrics.get(name, 0.0)

    def is_available(self) -> bool:
        """Check if metrics collection is available"""
        return True
