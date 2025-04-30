"""
Pulsar Exceptions Module
=========================
This module defines custom exceptions for the Pulsar library.
These exceptions are used to handle errors and issues that may arise during the execution of Pulsar stages.
"""

from typing import Optional


class PulsarException(Exception):
    """Base class for all Pulsar exceptions."""
    pass

class PulsarStageError(PulsarException):
    """Exception raised for errors in the Pulsar stage."""
    pass

class PulsarStageNotFoundError(PulsarStageError):
    """Exception raised when a specified Pulsar stage is not found."""
    def __init__(self, stage_name):
        self.stage_name = stage_name
        super().__init__(f"Pulsar stage '{stage_name}' not found.")

class PulsarStageAlreadyExistsError(PulsarStageError):
    """Exception raised when a Pulsar stage already exists."""
    def __init__(self, stage_name):
        self.stage_name = stage_name
        super().__init__(f"Pulsar stage '{stage_name}' already exists.")

class PulsarStageNotImplementedError(PulsarStageError):
    """Exception raised when a Pulsar stage is not implemented."""
    def __init__(self, stage_name):
        self.stage_name = stage_name
        super().__init__(f"Pulsar stage '{stage_name}' is not implemented.")

class PulsarStageTimeoutError(PulsarStageError):
    """Exception raised when a Pulsar stage times out."""
    def __init__(self, stage_name, timeout):
        self.stage_name = stage_name
        self.timeout = timeout
        super().__init__(f"Pulsar stage '{stage_name}' timed out after {timeout} seconds.")

class PulsarStageInvalidParameterError(PulsarStageError):
    """Exception raised when a Pulsar stage receives invalid parameters."""
    def __init__(self, stage_name, parameter, message):
        self.stage_name = stage_name
        self.parameter = parameter
        self.message = message
        super().__init__(f"Pulsar stage '{stage_name}' received invalid parameter: '{parameter}'. {message}")

class PulsarStageExecutionError(PulsarStageError):
    """Exception raised when a Pulsar stage execution fails."""
    def __init__(self, stage_name, error_message):
        self.stage_name = stage_name
        self.error_message = error_message
        super().__init__(f"Pulsar stage '{stage_name}' execution failed: {error_message}.")

class PulsarStageDependencyError(PulsarStageError):
    """Exception raised when a Pulsar stage has unmet dependencies."""
    def __init__(self, stage_name, dependency, message: Optional[str] = None):
        self.stage_name = stage_name
        self.dependency = dependency
        super().__init__(f"Pulsar stage '{stage_name}' has unmet dependency: '{dependency}'.")

class PulsarStageConfigurationError(PulsarStageError):
    """Exception raised when a Pulsar stage has configuration errors."""
    def __init__(self, stage_name, config):
        self.stage_name = stage_name
        self.config = config
        super().__init__(f"Pulsar stage '{stage_name}' has configuration errors: '{config}'.")

class PulsarStageExecutionTimeoutError(PulsarStageError):
    """Exception raised when a Pulsar stage execution times out."""
    def __init__(self, stage_name, timeout):
        self.stage_name = stage_name
        self.timeout = timeout
        super().__init__(f"Pulsar stage '{stage_name}' execution timed out after {timeout} seconds.")
class PulsarStageExecutionFailureError(PulsarStageError):
    """Exception raised when a Pulsar stage execution fails."""
    def __init__(self, stage_name, error_message):
        self.stage_name = stage_name
        self.error_message = error_message
        super().__init__(f"Pulsar stage '{stage_name}' execution failed: {error_message}.")

class PulsarStageExecutionAbortedError(PulsarStageError):
    """Exception raised when a Pulsar stage execution is aborted."""
    def __init__(self, stage_name):
        self.stage_name = stage_name
        super().__init__(f"Pulsar stage '{stage_name}' execution aborted.")

class PulsarStageExecutionCancelledError(PulsarStageError):
    """Exception raised when a Pulsar stage execution is cancelled."""
    def __init__(self, stage_name):
        self.stage_name = stage_name
        super().__init__(f"Pulsar stage '{stage_name}' execution cancelled.")

class PulsarStageExecutionSkippedError(PulsarStageError):
    """Exception raised when a Pulsar stage execution is skipped."""
    def __init__(self, stage_name):
        self.stage_name = stage_name
        super().__init__(f"Pulsar stage '{stage_name}' execution skipped.")

class PulsarStageExecutionNotStartedError(PulsarStageError):
    """Exception raised when a Pulsar stage execution has not started."""
    def __init__(self, stage_name):
        self.stage_name = stage_name
        super().__init__(f"Pulsar stage '{stage_name}' execution not started.")
