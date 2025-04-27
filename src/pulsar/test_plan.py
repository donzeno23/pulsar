import sys

from testplan import test_plan
from testplan.testing.multitest import MultiTest

from pulsar.tests.test_suite import StageTestSuite, StageTestSuite2


@test_plan(name="Pulsar Test Plan")
def main(plan):
    test = MultiTest(
            name="Pulsar MultiTest",
            suites=[
                StageTestSuite(),
                StageTestSuite2(),
            ],
        )
    plan.add(test)
    
if __name__ == "__main__":
    sys.exit(not main())