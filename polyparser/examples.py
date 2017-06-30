from poly_parser import Parser

parser = Parser()

output = parser.parse("2 ^ x").evaluate({"x": 2})
print(output)