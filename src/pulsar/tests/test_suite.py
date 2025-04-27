# pulsar/tests/test_suite.py
from rich import print as rprint

from testplan.testing.multitest import testsuite, testcase

from pulsar.stages.factory import StageFactory, setup_stages
from pulsar.core.dependencies import Logger, Producer, Metrics
from pulsar.stages.get_logs import GetLogsStage
from pulsar.stages.send_messages import SendMessagesStage
from pulsar.utils.helpers import print_stages, init_stage_dependencies, setup_test_dependencies

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
            rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{stage.name}[/yellow]")
            result.log(f"Running stage: {stage.name}")
            # Call the setup method of each stage
            stage.setup(env=env, result=result)

        rprint("[bold blue]Pulsar stages setup successfully![/bold blue]")
        result.log("Pulsar stages setup successfully")
    

    @testcase(parameters=[
        {"log_type": "snowflake", "limit": 20},
        {"log_type": "mongodb", "limit": 10},
    ])
    def run(self, env, result, log_type, limit):
        """Test the get_logs stage with different parameters."""
        testcase_params={"log_type": log_type, "limit": limit}
        rprint(f"[bold blue]Using parameters: {testcase_params}[/bold blue]")

        # Find and run get_logs stage
        get_logs_stage = next(
            (stage for stage in self.stages if stage.name == "get_logs"),
            None
        )
        if get_logs_stage:
            rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{get_logs_stage.name}[/yellow]")
            result.log(f"Running stage: {get_logs_stage.name}")
            get_logs_stage.run(params=testcase_params, env=env, result=result)
            rprint(f"[bold green]Stage {get_logs_stage.name} completed successfully![/bold green]")
            result.log(f"Stage {get_logs_stage.name} completed successfully!")
        
        # Run send_messages stage
        send_messages_stage = next(
            (stage for stage in self.stages if stage.name == "send_messages"),
            None
        )
        if send_messages_stage:
            send_messages_params = {"num_messages": 10, "duration": 5}
            rprint(f"[bold blue]Using parameters: {send_messages_params}[/bold blue]")
            rprint(f"[bold blue]Running stage:[/bold blue] [yellow]{send_messages_stage.name}[/yellow]")
            result.log(f"Running stage: {send_messages_stage.name}")
            send_messages_stage.run(params=send_messages_params, env=env, result=result)
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
                params={"num_messages": num_messages, "duration": duration},
                env=env,
                result=result
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
                stage.run(params=params, env=env, result=result)
            else:
                rprint(f"[bold blue]No parameters provided for stage: {stage.name}[/bold blue]")
                stage.run(env=env, result=result)
            stage.run(env=env, result=result)

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
            stage.run(
                params={"num_messages": num_messages, "duration": duration},
                env=env,
                result=result
            )

        rprint(f"[bold green]Sent {num_messages} messages successfully![/bold green]")

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


# For testing with mock dependencies
def setup_test_dependencies():
    """Set up mock dependencies for testing."""
    from pulsar.tests.mock_dependencies import MockLogger, MockProducer, MockMetrics
    
    factory = StageFactory()
    factory.register_dependency("logger", MockLogger())
    factory.register_dependency("producer", MockProducer())
    factory.register_dependency("metrics", MockMetrics())
    return factory

@testsuite(name="Test Suite with Mock Dependencies")
class MockStageTestSuite(StageTestSuite2):
    """A test suite using mock dependencies."""
    
    def _setup_dependencies(self, env):
        """Override to use mock dependencies."""
        # Set up mock dependencies using helper
        mock_deps = setup_test_dependencies(self.factory)
        
        # Initialize dependencies for each stage
        init_stage_dependencies(
            self.factory,
            GetLogsStage,
            logger=mock_deps["logger"]
        )

        init_stage_dependencies(
            self.factory,
            SendMessagesStage,
            producer=mock_deps["producer"],
            metrics=mock_deps["metrics"],
            logger=mock_deps["logger"]
        )