from poly_parser import Parser
import os
import xml.etree.ElementTree as et
import numpy as np
import random

class function_utilities():

    class Reader():

        def __init__(self, file):
            self.expression = ""
            self.type = "hidden"
            self.errormsg = ""
            self.exprfile = file


        def readexpr(self, type = "hidden"):
            expr_file = self.exprfile
            exptree = et.parse(expr_file)
            rt = exptree.getroot()
            expr = ""
            for functions in rt.findall("function"):
                if functions.find("type").text == type:
                    expr = functions.find("expression").text
            if expr == "":
                self.errormsg = "no expression found"
                raise Exception(self.errormsg)
            self.expression = expr


    class Writer():

        def __init__(self, expr_file):
            self.expression = ""
            self.type = ""
            self.exprfile = expr_file

        def writeexpr(self, expression, type = "hidden"):
            expr_file = self.exprfile
            self.expression = expression
            if os.path.isfile(expr_file):
                exptree = et.parse(expr_file)
                rt = exptree.getroot()
                for functions in rt.findall("function"):
                    if functions.find("type").text == type:
                        functions.find("expression").text = expression
                exptree.write(expr_file)


    class PolyGen():

        def __init__(self):
            self.expression = ""

        def generatepoly(self, vars, domain, degree, terms):
            expression = ""
            coeff = np.random.uniform(domain[0], domain[1], terms-1)
            terms_degree = np.random.random_integers(1, degree, terms-1)
            coeff_0 = np.random.uniform(domain[0], domain[1])
            L = len(vars)
            expression = str(coeff_0)
            for i in range(0, L):
                expression = expression + "+" + str(coeff[i]) + "*" + vars[i] + "^" + str(terms_degree[i])

            for i in range(L, len(terms_degree)):
                expr_tmp = ""
                for j in range(1, terms_degree[i]+1):
                    next_term = np.random.randint(0, L)
                    if expr_tmp != "":
                        expr_tmp = expr_tmp + "*" + vars[next_term]
                    else:
                        expr_tmp = vars[next_term]
                expression = expression + "+" + expr_tmp

            return expression

    class Evaluator():

        def __init__(self, expr_file):
            self.exprfile = expr_file
            self.type = "hidden"


        def eval_function(self, values):
            parser = Parser()
            # read function expression
            expreader = function_utilities.Reader(self.exprfile)
            expreader.readexpr(self.type)
            # parse the expression and evaluate

            expr = parser.parse(expreader.expression)
            variables = expr.variables()

            input = dict()

            i = 0
            for idx in variables:
                input[idx] = values[i]
                i += 1

            return expr.evaluate(input)




