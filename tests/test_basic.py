# -*- coding: utf-8 -*-

from polyparser.poly_parser import Parser

import unittest
from polyparser.func_util import function_utilities
from polyparser import poly_parser

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_read_polynomial(self):
        expwriter = function_utilities.Writer("func.xml")
        expwriter.writeexpr("x ^ 2")
        expreader = function_utilities.Reader("func.xml")
        expreader.readexpr("hidden")

        self.assertTrue(expreader.expression == "x ^ 2")

        expwriter.writeexpr("x ^ 3")
        expreader.readexpr("hidden")

        self.assertFalse(expreader.expression == "x ^ 2")

    def test_write_polynomial(self):
        expwrite = function_utilities.Writer("func.xml")
        expwrite.writeexpr("x*y")

        self.assertTrue(expwrite.expression == "x*y")

    def test_parser(self):
        parser = Parser()

        expwrite = function_utilities.Writer("func.xml")
        expwrite.writeexpr("x * y")
        expreader = function_utilities.Reader("func.xml")
        expreader.readexpr("hidden")

        output = parser.parse(expreader.expression).evaluate({"x":2, "y": 4})

        self.assertTrue(output == 8)

    def test_absolute_truth_and_meaning(self):
        assert True



# if __name__ == '__main__':
#     unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(BasicTestSuite)
unittest.TextTestRunner(verbosity=2).run(suite)

