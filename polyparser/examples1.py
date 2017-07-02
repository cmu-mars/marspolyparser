from func_util import function_utilities

poly = function_utilities.PolyGen()

poly_example = poly.generatepoly(("x", "y"), [0, 10], 3, 10)

print(poly_example)