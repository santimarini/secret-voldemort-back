import unittest
import UserTest
import GameTest

#initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add test to the test suite
suite.addTest(loader.loadTestsFromModule(UserTest))
# suite.addTest(loader.loadTestsFromModule(GameTest))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)