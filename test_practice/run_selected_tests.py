import unittest
from test_add import TestAdd
from test_subtract import TestSubtract


suite = unittest.TestSuite()

suite.addTest(TestAdd("test_add_positive"))
suite.addTest(TestSubtract("test_subtract_negative"))

runner = unittest.TextTestRunner()
runner.run(suite)