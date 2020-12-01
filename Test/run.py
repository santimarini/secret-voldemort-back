import unittest
import UserTest
import GameTest
import GameInitTest
import CardsTest
from mock_database import *

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add test to the test suite
suite.addTest(loader.loadTestsFromModule(UserTest))
suite.addTest(loader.loadTestsFromModule(GameTest))
suite.addTest(loader.loadTestsFromModule(GameInitTest))
suite.addTest(loader.loadTestsFromModule(CardsTest))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
