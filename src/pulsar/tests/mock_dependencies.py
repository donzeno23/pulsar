# pulsar/tests/mock_dependencies.py
from pulsar.core.dependencies import BaseDependency


class MockLogger(BaseDependency):
    def __init__(self):
        self.logs = []

    def info(self, msg):
        self.logs.append(("info", msg))

    def is_available(self):
        return True

class MockProducer(BaseDependency):
    def __init__(self):
        self.messages = []
        self._connected = True

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

    def send_message(self, msg):
        if not self._connected:
            raise RuntimeError("Producer not connected")
        self.messages.append(msg)

    def is_available(self):
        return self._connected
        # Simulate availability for testing purposes
        # return True

class MockMetrics(BaseDependency):
    def __init__(self):
        self.metrics = {}

    def record_send(self, value=1.0, tags=None):
        self.metrics["messages.sent"] = self.metrics.get("messages.sent", 0) + value

    def is_available(self):
        return True
