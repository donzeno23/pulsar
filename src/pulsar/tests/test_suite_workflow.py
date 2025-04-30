# pulsar/tests/test_suite.py
from typing import Optional, Dict, Any
from rich import print as rprint
from testplan.testing.multitest import testsuite, testcase

from pulsar.core.builder import WorkflowBuilder
from pulsar.core.observer import LoggingObserver
from pulsar.core.models import StageStatus
from pulsar.core.dependencies import Logger, Producer, Metrics
from pulsar.stages.get_logs import GetLogsStage
from pulsar.stages.send_messages import SendMessagesStage
from pulsar.utils.helpers import create_context

@testsuite(name="Workflow Test Suite")
class WorkflowTestSuite:
    """Test suite demonstrating workflow execution with proper lifecycle management"""

    def setup(self, env: Dict[str, Any], result: Any) -> None:
        """Set up the test suite by initializing workflow and stages"""
        result.log("Setting up workflow test suite...")
        rprint("[bold blue]Setting up workflow test suite...[/bold blue]")

        try:
            # Create dependencies
            logger = Logger()
            producer = Producer()
            metrics = Metrics()

            # Create observers
            logging_observer = LoggingObserver(logger)

            # Create stages
            get_logs = GetLogsStage()
            send_messages = SendMessagesStage()

            # Add observers to stages
            get_logs.add_observer(logging_observer)
            send_messages.add_observer(logging_observer)

            # Set up stage dependencies
            GetLogsStage.set_dependencies(logger=logger)
            SendMessagesStage.set_dependencies(
                producer=producer,
                metrics=metrics,
                logger=logger
            )

            # Create and configure workflow
            workflow_builder = WorkflowBuilder("test_workflow")
            self.workflow = (
                workflow_builder
                .add_stage(get_logs)
                .add_stage(send_messages, depends_on=[get_logs.name])
                .build()
            )

            # Set up workflow with context
            setup_context = create_context(env, result)
            self.workflow.setup(env=setup_context.get('env'), result=setup_context.get('result'))

            result.log("Workflow setup completed successfully")
            rprint("[bold green]Workflow setup completed successfully[/bold green]")

        except Exception as e:
            error_msg = f"Failed to set up workflow: {str(e)}"
            result.log(error_msg)
            rprint(f"[bold red]{error_msg}[/bold red]")
            raise

    @testcase(parameters=[
        {"num_messages": 10, "log_type": "application", "limit": 100},
        {"num_messages": 20, "log_type": "security", "limit": 200},
    ])
    def test_workflow_execution(self, env: Dict[str, Any], result: Any, 
                              log_type: str, limit: int, num_messages: int) -> None:
        """Test workflow execution with different parameters"""

        result.log(f"Running workflow test with parameters: log_type={log_type}, "
                  f"limit={limit}, num_messages={num_messages}")
        rprint(f"[bold blue]Running workflow test with parameters: "
               f"log_type={log_type}, limit={limit}, num_messages={num_messages}[/bold blue]")

        try:
            # Create context with test parameters
            context = create_context(
                env=env,
                result=result,
                log_type=log_type,
                limit=limit,
                num_messages=num_messages,
                duration=5  # Fixed duration for this example
            )

            # Execute workflow
            workflow_result = self.workflow.execute(context)

            # Handle workflow result
            if workflow_result.status == StageStatus.FAILED:
                error_msg = f"Workflow execution failed: {workflow_result.error}"
                result.log(error_msg)
                result.fail(f"Stage: '{workflow_result.stage_name}' has failed, with error: {workflow_result.error} ")
                rprint(f"[bold red]{error_msg}[/bold red]")
                raise workflow_result.error

            # Log success
            success_msg = (f"Workflow completed successfully - Retrieved {limit} {log_type} logs "
                         f"and sent {num_messages} messages")
            result.log(success_msg)
            rprint(f"[bold green]{success_msg}[/bold green]")

        except Exception as e:
            error_msg = f"Error during workflow execution: {str(e)}"
            result.log(error_msg)
            rprint(f"[bold red]{error_msg}[/bold red]")
            raise

    def teardown(self, env: Dict[str, Any], result: Any) -> None:
        """Clean up workflow and resources"""
        result.log("Tearing down workflow test suite...")
        rprint("[bold blue]Tearing down workflow test suite...[/bold blue]")

        try:
            # Create teardown context
            teardown_context = create_context(env, result)
            
            # Teardown workflow
            self.workflow.teardown(
                env=teardown_context.get('env'),
                result=teardown_context.get('result')
            )

            result.log("Workflow teardown completed successfully")
            rprint("[bold green]Workflow teardown completed successfully[/bold green]")

        except Exception as e:
            error_msg = f"Failed to tear down workflow: {str(e)}"
            result.log(error_msg)
            rprint(f"[bold red]{error_msg}[/bold red]")
            raise
