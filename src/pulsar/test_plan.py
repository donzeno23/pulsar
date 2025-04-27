import sys

from testplan import test_plan
from testplan.testing.multitest import MultiTest

from pulsar.tests.test_suite import StageTestSuite1, StageTestSuite2, PulsarMessageTestSuite, MockStageTestSuite


@test_plan(name="Pulsar Test Plan")
def main(plan):
    # test = MultiTest(
    #         name="Pulsar MultiTest",
    #         suites=[
    #             StageTestSuite(),
    #             # StageTestSuite2(),
    #         ],
    #     )
    # plan.add(test)

    # Running with real dependencies
    multitest = MultiTest(
        name="Pulsar Stages Test",
        suites=[StageTestSuite1(), StageTestSuite2(), PulsarMessageTestSuite()]
    )

    # Running with mock dependencies
    multitest_mock = MultiTest(
        name="Pulsar Stages Mock Test",
        suites=[MockStageTestSuite()]
    )
    plan.add(multitest)
    plan.add(multitest_mock)

    
if __name__ == "__main__":
    sys.exit(not main())