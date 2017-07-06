from poly_parser import Parser
from func_util import function_utilities

parser = Parser()

expwriter = function_utilities.Writer("func.xml")
expwriter.writeexpr("x ^ 3 + y")

expreader = function_utilities.Reader("func.xml")
expreader.readexpr("hidden")

eval = function_utilities.Evaluator("func.xml")
print(eval.eval_function([2,3]))

expr = parser.parse(expreader.expression)

print(expr.variables())

output = parser.parse(expreader.expression).evaluate({"x": 3})
output1 = parser.parse(expwriter.expression).evaluate({"x": 2})


print(output)