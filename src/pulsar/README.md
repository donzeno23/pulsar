# Pulsar Toolkit

A high-performance testing and workflow automation toolkit built with Python, designed for creating modular, observable, and maintainable test workflows.

## 🚀 Features

- Modular stage-based architecture
- Dependency injection and management
- Observable workflow execution
- Composable test workflows
- Rich logging and metrics
- Parameterized testing support
- Flexible configuration

## 📋 Table of Contents

- [Pulsar Toolkit](#pulsar-toolkit)
  - [🚀 Features](#-features)
  - [📋 Table of Contents](#-table-of-contents)
  - [🔧 Installation](#-installation)
    - [Prerequisites](#prerequisites)
    - [Setup Environment](#setup-environment)
  - [🚀 Quick Start](#-quick-start)
  - [🏗 Architecture](#-architecture)
    - [Pulsar is built on several key design patterns](#pulsar-is-built-on-several-key-design-patterns)
  - [📦 Creating New Stages](#-creating-new-stages)
  - [Create a new file in pulsar/stages/](#create-a-new-file-in-pulsarstages)
  - [Register stage dependencies](#register-stage-dependencies)
  - [✅ Writing Test Suites](#-writing-test-suites)
    - [Create a new test suite](#create-a-new-test-suite)
  - [🔗 Managing Dependencies](#-managing-dependencies)
  - [Define stage dependencies](#define-stage-dependencies)
  - [Create dependency instances](#create-dependency-instances)
  - [Set dependencies](#set-dependencies)
  - [Access in stage](#access-in-stage)
  - [💡 Best Practices](#-best-practices)
  - [📚 API Reference](#-api-reference)
    - [Core Components](#core-components)
    - [Stage Lifecycle](#stage-lifecycle)
    - [Context Dictionary](#context-dictionary)
    - [🤝 Contributing](#-contributing)
    - [📝 License](#-license)
    - [👥 Authors](#-authors)
    - [🙏 Acknowledgments](#-acknowledgments)

## 🔧 Installation

### Prerequisites

- Python 3.10+
- uv package manager (recommended)

### Setup Environment

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/yourusername/pulsar.git
cd pulsar

# Create virtual environment and install dependencies
cd src
uv venv
source .venv/bin/activate
uv pip install -e .
```

## 🚀 Quick Start

```python
from pulsar.core.builder import WorkflowBuilder
from pulsar.stages.get_logs import GetLogsStage
from pulsar.stages.send_messages import SendMessagesStage

# Create workflow
workflow = (
    WorkflowBuilder("my_workflow")
    .add_stage(GetLogsStage())
    .add_stage(SendMessagesStage(), depends_on=["get_logs"])
    .build()
)

# Execute workflow
result = workflow.execute(context={
    "params": {
        "log_type": "application",
        "limit": 100
    }
})
```

## 🏗 Architecture

### Pulsar is built on several key design patterns

- Command Pattern : Each stage is a command object
- Observer Pattern : Stages notify observers of state changes
- Composite Pattern : Workflows compose stages into DAGs
- Builder Pattern : Fluent API for workflow construction
- Dependency Injection : Clean dependency management

## 📦 Creating New Stages

## Create a new file in pulsar/stages/

```python
# pulsar/stages/my_stage.py
from typing import Dict, Any
from pulsar.stages.base_stage import BaseStage

class MyStage(BaseStage):
    name = "my_stage"
    dependencies = ["logger", "metrics"]
    optional = False
    
    metadata = {
        "description": "My custom stage",
        "version": "1.0.0",
        "author": "Your Name",
        "tags": ["custom"]
    }
    
    def run(self, context: Dict[str, Any]) -> Any:
        logger = self.get_deps()["logger"]
        metrics = self.get_deps()["metrics"]
        
        params = context.get("testcase_params", context)
        value = params.get("value", "default")
        
        logger.info(f"Processing value: {value}")
        metrics.record_execution(1.0)
        
        return {"result": value}
```

## Register stage dependencies

```python
from pulsar.core.dependencies import Logger, Metrics

MyStage.set_dependencies(
    logger=Logger(),
    metrics=Metrics()
)
```

## ✅ Writing Test Suites

### Create a new test suite

```python
# pulsar/tests/test_my_stage.py
from testplan.testing.multitest import testsuite, testcase
from pulsar.core.builder import WorkflowBuilder
from pulsar.core.observer import LoggingObserver
from pulsar.core.models import StageStatus
from pulsar.stages.my_stage import MyStage

@testsuite(name="My Stage Test Suite")
class MyStageTestSuite:
    def setup(self, env, result):
        """Initialize workflow and stages"""
        result.log("Setting up test suite...")
        
        # Create workflow
        workflow_builder = WorkflowBuilder("test_workflow")
        self.workflow = (
            workflow_builder
            .add_stage(MyStage())
            .build()
        )
        
        # Setup workflow
        self.workflow.setup(env=env, result=result)
    
    @testcase(parameters=[
        {"value": "test1"},
        {"value": "test2"}
    ])
    def test_my_stage(self, env, result, value):
        """Test stage with different parameters"""
        context = {
            "env": env,
            "result": result
            "value": value
        }
        
        workflow_result = self.workflow.execute(context)
        
        if workflow_result.status == StageStatus.FAILED:
            raise workflow_result.error
            
        result.log(f"Stage executed successfully with value: {value}")
    
    def teardown(self, env, result):
        """Clean up resources"""
        self.workflow.teardown(env=env, result=result)
```

## 🔗 Managing Dependencies

## Define stage dependencies

```python
class MyStage(BaseStage):
    dependencies = ["logger", "metrics"]
```

## Create dependency instances

```python
from pulsar.core.dependencies import Logger, Metrics

logger = Logger()
metrics = Metrics()
```

## Set dependencies

```python
MyStage.set_dependencies(
    logger=logger,
    metrics=metrics
)
```

## Access in stage

```python
def run(self, context):
    logger = self.get_deps()["logger"]
    metrics = self.get_deps()["metrics"]
```

## 💡 Best Practices

1. **Stage Design**

   - Keep stages focused and single-purpose
   - Use meaningful names and descriptions
   - Document parameters and return values
   - Handle errors gracefully

2. **Dependencies**

   - Minimize dependencies between stages
   - Use dependency injection
   - Document required dependencies
   - Provide sensible defaults

3. **Testing**

   - Write parameterized tests
   - Test edge cases
   - Use meaningful test data
   - Clean up resources

## 📚 API Reference

### Core Components

- `WorkflowBuilder`: Constructs workflow DAGs
- `StageCommand`: Base command pattern implementation
- `CompositeStage`: Manages stage composition
- `StageObserver`: Monitors stage execution

### Stage Lifecycle

1. `setup()`: Initialize resources
2. `execute()`: Run stage logic
3. `teardown()`: Clean up resources

### Context Dictionary

```python
context = {
    "params": dict,    # Stage parameters
    "env": dict,       # Environment variables
    "result": object   # Test result object
}
```

### 🤝 Contributing

1. Fork the repository

2. Create a feature branch

3. Commit your changes

4. Push to the branch

5. Create a Pull Request

### 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

### 👥 Authors

- Michael Daloia - Initial work - GitHub

### 🙏 Acknowledgments

- List any inspirations

- Credits to contributors

- Links to similar projects

For more information, please visit our documentation.