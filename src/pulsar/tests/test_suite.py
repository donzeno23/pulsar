# pulsar/tests/test_suite.py
from rich import print as rprint

from testplan.testing.multitest import testsuite, testcase

from pulsar.core.factory import StageFactory, setup_stages
from pulsar.core.dependencies import Logger, Producer, Metrics
from pulsar.core.observer import LoggingObserver
# from pulsar.core.composite import CompositeStage
from pulsar.core.builder import WorkflowBuilder
from pulsar.core.models import StageStatus
from pulsar.stages.get_logs import GetLogsStage
from pulsar.stages.send_messages import SendMessagesStage
from pulsar.utils.helpers import print_stages, init_stage_dependencies, setup_test_dependencies, create_context

from pulsar.stages import get_logs, send_messages


@testsuite(name="Pulsar Stage Test Suite Using Directly")
class StageTestSuite1(object):

    def setup(self, env, result):
        GetLogsStage.set_dependencies(logger=Logger())
        SendMessagesStage.set_dependencies(
            producer=Producer(),
            metrics=Metrics(),
            logger=Logger()
        )
        rprint("[bold blue]Setting up the test suite...[/bold blue]")
        result.log("Setting up the test suite...")
        rprint("[bold green]Pulsar stages initialized successfully![/bold green]")

        # Store the stage classes (not modules)
        self.stages = [GetLogsStage, SendMessagesStage]

        print_stages(self.stages)
        # Execute the setup method for each stage
        for stage in self.stages:
            rprint(f"[bold blue]Running setup for stage:[/bold blue] [yellow]{stage.name}[/yellow]")
            result.log(f"Running setup for stage: {stage.name}")
            # Call the setup method of each stage
            stage.setup(env=env, result=result)

        rprint("[bold blue]Pulsar stages setup successfully![/bold blue]")
        result.log("Pulsar stages setup successfully")
    

    @testcase(parameters=[
        {"num_messages": 100, "duration": 10, "log_type": "snowflake", "limit": 20},
        {"num_messages": 200, "duration": 20, "log_type": "mongodb", "limit": 10},
    ])
    def run(self, env, result, num_messages, duration, log_type, limit):
        """Test the get_logs stage with different parameters."""

        context = create_context(
            env=env,
            result=result,
            num_messages=num_messages,
            duration=duration,
            log_type=log_type,
            limit=limit,                
        )
        # Find and run get_logs stage
        get_logs_stage = next(
            (stage for stage in self.stages if stage.name == "get_logs"),
            None
        )
        if get_logs_stage:
            rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{get_logs_stage.name}[/yellow]")
            result.log(f"Running stage: {get_logs_stage.name}")

            get_logs_stage.run(context=context)
            rprint(f"[bold green]Stage {get_logs_stage.name} completed successfully![/bold green]")
            result.log(f"Stage {get_logs_stage.name} completed successfully!")
        
        # Run send_messages stage
        send_messages_stage = next(
            (stage for stage in self.stages if stage.name == "send_messages"),
            None
        )
        if send_messages_stage:
            rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{send_messages_stage.name}[/yellow]")
            result.log(f"Running stage: {send_messages_stage.name}")

            rprint(f"[bold blue]Using parameters: {context}[/bold blue]")
            result.log(f"Using parameters: {context}")

            send_messages_stage.run(context=context)
            rprint(f"[bold green]Stage {send_messages_stage.name} completed successfully![/bold green]")
            result.log(f"Stage {send_messages_stage.name} completed successfully!")
    
    def teardown(self, env, result):
        """Tear down all stages."""
        rprint("[bold red]Tearing down the test suite...[/bold red]")
        result.log("Tearing down the test suite...")
        
        for stage in self.stages:
            try:
                stage.teardown(env=env, result=result)
                result.log(f"Stage {stage.name} torn down successfully")
            except Exception as e:
                result.log(f"Error tearing down stage {stage.name}: {str(e)}")
                if not stage.optional:
                    raise

        rprint("[bold green]Pulsar stages torn down successfully![/bold green]")
        result.log("Pulsar stages torn down successfully")
        rprint("[bold red]Test suite torn down successfully![/bold red]")

@testsuite(name="Test Suite for Pulsar Stage Using Factory")
class StageTestSuite2(object):
    """A test suite for the Pulsar stage."""

    def setup(self, env, result):
        """Set up the test suite by initializing stages with dependencies."""
        rprint("[bold blue]Setting up the test suite...[/bold blue]")
        result.log("Setting up the test suite...")

        # Create and configure the factory
        self.factory = StageFactory()
        
        # Register dependencies and initialize stages
        self._setup_dependencies(env)
                
        # Initialize all stages
        self.stages = self._initialize_stages(result)
        
        rprint("[bold green]Pulsar stages initialized successfully![/bold green]")
        print_stages(self.stages)

        # Execute the setup method for each stage
        for stage in self.stages:
            stage.setup(env=env, result=result)

    def _setup_dependencies(self, env):
        """Set up and register all dependencies."""

        # Create dependencies
        logger = Logger()
        producer = Producer()
        metrics = Metrics()

        # Initialize dependencies for each stage using helper
        init_stage_dependencies(
            self.factory,
            GetLogsStage,
            logger=logger
        )

        init_stage_dependencies(
            self.factory,
            SendMessagesStage,
            producer=producer,
            metrics=metrics,
            logger=logger
        )


    def _register_stages(self):
        """Register all available stages with the factory."""
        
        self.factory.register_stage(GetLogsStage)
        self.factory.register_stage(SendMessagesStage)

    def _initialize_stages(self, result):
        """Initialize all registered stages."""
        available_stages = []

        self._register_stages()

        # Initialize each stage and check if it's available        
        for stage_name in self.factory._stage_classes:
            try:
                stage = self.factory.create_stage(stage_name)
                if stage.is_available():
                    available_stages.append(stage)
                    result.log(f"Stage {stage_name} initialized successfully")
                else:
                    msg = f"Optional stage {stage_name} skipped - dependencies not met"
                    rprint(f"[yellow]{msg}[/yellow]")
                    result.log(msg)
            except Exception as e:
                result.log(f"Failed to initialize stage {stage_name}: {str(e)}")
                if not stage.optional:
                    raise
        
        return available_stages

    @testcase(parameters=[
        {"num_messages": 10, "duration": 5},
        {"num_messages": 20, "duration": 10},
        {"num_messages": 30, "duration": 15},
        {"num_messages": 40, "duration": 20},
        {"num_messages": 50, "duration": 25},
    ])
    def test_send_messages(self, env, result, num_messages, duration):
        """Test sending messages with different parameters."""
        rprint(f"[bold blue]Sending {num_messages} messages...[/bold blue]")
        
        for stage in self.stages:
            # Skip specific stages if needed
            if stage.name == "get_logs":
                rprint(f"[bold red]Skipping stage: {stage.name}[/bold red]")
                continue
                
            rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{stage.name}[/yellow]")
            stage.run(
                context=create_context(
                    env=env,
                    result=result,
                    num_messages=num_messages,
                    duration=duration
                )
            )
            
        rprint(f"[bold green]Sent {num_messages} messages successfully![/bold green]")

    @testcase
    def test_run(self, env, result):
        """Test running all stages in sequence."""
        result.log("Running all stages...")
        
        for stage in self.stages:
            rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{stage.name}[/yellow]")
            if stage.name == "get_logs":
                params = {"log_type": "application", "limit": 100}
                rprint(f"[bold blue]Using parameters: {params}[/bold blue]")
                stage.run(context=create_context(
                    env=env,
                    result=result,
                    params=params
                ))
            else:                
                stage.run(context=create_context(
                    env=env,
                    result=result,
                ))
            rprint(f"[bold green]Stage {stage.name} completed successfully![/bold green]")
            

    def teardown(self, env, result):
        """Tear down all stages."""
        rprint("[bold red]Tearing down the test suite...[/bold red]")
        result.log("Tearing down the test suite...")
        
        for stage in self.stages:
            try:
                stage.teardown(env=env, result=result)
                result.log(f"Stage {stage.name} torn down successfully")
            except Exception as e:
                result.log(f"Error tearing down stage {stage.name}: {str(e)}")
                if not stage.optional:
                    raise

@testsuite(name="Pulsar Message Test Suite")
class PulsarMessageTestSuite(object):
    """Test suite for Pulsar message sending functionality."""

    def setup(self, env, result):
        """Set up the test suite by initializing stages with dependencies."""
        rprint("[bold blue]Setting up the test suite...[/bold blue]")
        result.log("Setting up the test suite...")

        stages = [
            GetLogsStage,
            SendMessagesStage
        ]

        # Setup stages using factory helper
        try:
            self.stages = setup_stages()
            rprint("[bold green]Pulsar stages initialized successfully![/bold green]")
            print_stages(self.stages)
            result.log("Stages initialized successfully")
            for stage in self.stages:
                stage.setup(env=env, result=result)
        except Exception as e:
            error_msg = f"Failed to setup stages: {str(e)}"
            result.log(error_msg)
            rprint(f"[bold red]{error_msg}[/bold red]")
            raise

    @testcase(parameters=[
        {"num_messages": 10, "duration": 5},
        {"num_messages": 20, "duration": 10},
        {"num_messages": 30, "duration": 15},
        {"num_messages": 40, "duration": 20},
        {"num_messages": 50, "duration": 25},
    ])
    def test_send_messages(self, env, result, num_messages, duration):
        """Test sending messages with different parameters."""
        rprint(f"[bold blue]Sending {num_messages} messages...[/bold blue]")

        for stage in self.stages:
            rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{stage.name}[/yellow]")
            stage.run(context=create_context(
                env=env,
                result=result,
                num_messages=num_messages,
                duration=duration
            ))

        rprint(f"[bold green]Sent {num_messages} messages for a duration of {duration} seconds successfully![/bold green]")

    def teardown(self, env, result):
        """Tear down all stages."""
        rprint("[bold red]Tearing down the test suite...[/bold red]")
        result.log("Tearing down the test suite...")

        for stage in self.stages:
            try:
                stage.teardown(env=env, result=result)
                result.log(f"Stage {stage.name} torn down successfully")
            except Exception as e:
                result.log(f"Error tearing down stage {stage.name}: {str(e)}")
                if not stage.optional:
                    raise

@testsuite(name="Test Suite for Pulsar Stage Using Command")
class PulsarTestSuiteCommand(object):
    def setup(self, env, result):
        # Create observers
        logging_observer = LoggingObserver(Logger())

        # Create composite stage
        # self.workflow = CompositeStage(
        #     stages=[
        #         GetLogsStage(),
        #         SendMessagesStage()
        #     ],
        #     observers=[logging_observer]
        # )
        # self.workflow = CompositeStage("test_workflow")

        # Create workflow using builder
        workflow_builder = WorkflowBuilder("test_workflow")
        
        # Create and configure stages
        get_logs = GetLogsStage()
        send_messages = SendMessagesStage()
        
        # Add observers
        get_logs.add_observer(logging_observer)
        send_messages.add_observer(logging_observer)

        # Set up dependencies
        get_logs.set_dependencies(logger=Logger())
        send_messages.set_dependencies(
            producer=Producer(),
            metrics=Metrics(),
            logger=Logger()
        )
        # GetLogsStage.set_dependencies(logger=Logger())
        # SendMessagesStage.set_dependencies(
        #     producer=Producer(),
        #     metrics=Metrics(),
        #     logger=Logger()
        # )
        
        # # Add stages to workflow
        # self.workflow.add_substage(get_logs)
        # self.workflow.add_substage(send_messages)
        # # Set up dependencies between stages
        # send_messages.add_dependency(get_logs)

        # Build workflow with dependencies
        self.workflow = (
            workflow_builder
            .add_stage(get_logs)
            .add_stage(send_messages, depends_on=[get_logs.name]) # depends_on=["get_logs"]
            .build()
        )
        self.workflow.setup(env=env, result=result)

    @testcase(parameters=[
        {"num_messages": 500, "duration": 60, "log_type": "application", "limit": 100},
        {"num_messages": 250, "duration": 120, "log_type": "security", "limit": 200}
    ])
    def test_workflow(self, env, result, num_messages, duration, log_type, limit):
        testcase_params = {"log_type": log_type, "limit": limit }
        rprint(f"[bold blue]Using parameters: {testcase_params}[/bold blue]")
        context = create_context(
            env=env,
            result=result,
            num_messages=num_messages,
            duration=duration,
            log_type=log_type,
            limit=limit,
        )
        rprint(f"[bold blue]Running workflow with parameters: {context}[/bold blue]")
        result.log(f"Running workflow with parameters: {context}")
        
        workflow_result = self.workflow.execute(context)
        
        if workflow_result.status == StageStatus.FAILED:
            result.log(f"Workflow failed: {workflow_result.error}")
            raise workflow_result.error
        
        result.log("Workflow completed successfully")

    def teardown(self, env, result):
        # Tear down workflow
        self.workflow.teardown(env=env, result=result)
