from poly_parser import Parser
from func_util import function_utilities

parser = Parser()

expreader = function_utilities.Reader("func.xml")
expreader.readexpr("hidden")

expwriter = function_utilities.Writer("func.xml")
expwriter.writeexpr("x ^ 3")

output = parser.parse(expwriter.expression).evaluate({"x": 2})
print(output)