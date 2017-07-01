import os
import xml.etree.ElementTree as et

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



