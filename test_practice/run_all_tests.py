import unittest
from test_add import TestAdd
from test_subtract import TestSubtract


suite = unittest.TestSuite()

loader = unittest.TestLoader()
suite.addTest(loader.loadTestsFromTestCase(TestAdd))
suite.addTest(loader.loadTestsFromTestCase(TestSubtract))

runner = unittest.TextTestRunner()
runner.run(suite)