import math
import random

TNUMBER = 0
TOP1 = 1
TOP2 = 2
TVAR = 3
TFUNCALL = 4


class Token():

    def __init__(self, type_, index_, prio_, number_):
        self.type_ = type_
        self.index_ = index_ or 0
        self.prio_ = prio_ or 0
        self.number_ = number_ if number_ != None else 0

    def toString(self):
        if self.type_ == TNUMBER:
            return self.number_
        if self.type_ == TOP1 or self.type_ == TOP2 or self.type_ == TVAR:
            return self.index_
        elif self.type_ == TFUNCALL:
            return "CALL"
        else:
            return "Invalid Token"


class Expression():

    def __init__(self, tokens, ops1, ops2, functions):
        self.tokens = tokens
        self.ops1 = ops1
        self.ops2 = ops2
        self.functions = functions

    def simplify(self, values):
        values = values or {}
        nstack = []
        newexpression = []
        L = len(self.tokens)
        for i in range(0, L):
            item = self.tokens[i]
            type_ = item.type_
            if type_ == TNUMBER:
                nstack.append(item)
            elif type_ == TVAR and item.index_ in values:
                item = Token(TNUMBER, 0, 0, values[item.index_])
                nstack.append(item)
            elif type_ == TOP2 and len(nstack)>1:
                n2 = nstack.pop()
                n1 = nstack.pop()
                f = self.ops2[item.index_]
                item = Token(TNUMBER, 0, 0, f(n1.number_, n2.number_))
                nstack.append(item)
            elif type_ == TOP1 and nstack:
                n1 = nstack.pop()
                f = self.ops1[item.index_]
                item = Token(TNUMBER, 0, 0, f(n1.number_))
                nstack.append(item)
            else:
                while len(nstack) > 0:
                    newexpression.append(nstack.pop(0))
                newexpression.append(item)
        while nstack:
            newexpression.add(nstack.pop(0))

        return Expression(newexpression, self.ops1, self.ops2, self.functions)

    def evaluate(self, values):
        values = values or {}
        nstack = []
        L = len(self.tokens)
        for i in range(0, L):
            item = self.tokens[i]
            type_ = item.type_
            if type_ == TNUMBER:
                nstack.append(item.number_)
            elif type_ == TOP2:
                n2 = nstack.pop()
                n1 = nstack.pop()
                f = self.ops2[item.index_]
                nstack.append(f(n1, n2))
            elif type_ == TOP1:
                n1 = nstack.pop()
                f = self.ops1[item.index_]
                nstack.append(f(n1))
            elif type_ == TVAR:
                if item.index_ in values:
                    nstack.append(values[item.index_])
                elif item.index_ in self.functions:
                    nstack.append(self.functions[item.index_])
            elif type_ == TFUNCALL:
                n1 = nstack.pop()
                f = nstack.pop()
                if callable(f):
                    if type(n1) is list:
                        nstack.append(f(*n1))
                    else:
                        nstack.append(call(f, n1))
                else:
                    raise Exception(f + " is not a function")
            else:
                raise Exception("invalid expression")
        return nstack[0]

    def toString(self):
        nstack = []
        L = len(self.tokens)
        for i in range(0, L):
            item = self.tokens[i]
            type_ = item.type_
            if type_ == TNUMBER:
                if type(item.number_) == str:
                    nstack.append("'"+item.number_+"'")
                else:
                    nstack.append(item.number_)
            elif type_ == TOP2:
                n2 = nstack.pop()
                n1 = nstack.pop()
                f = item.index_
                frm = '({n1}{f}{n2})'

                nstack.append(frm.format(n1=n1, n2=n2, f=f))
            elif type_ == TOP1:
                n1 = nstack.pop()
                f = item.index_
                if f == "-":
                    nstack.append("(" + f + n1 + ")")
                else:
                    nstack.append(f + "(" + n1 + ")")
            elif type_ == TFUNCALL:
                n1 = nstack.pop()
                f = nstack.pop()
                nstack.append(f + "(" + n1 + ")")
            else:
                raise Exception("Invalid expression")
        return nstack[0]

    def variables(self):
        vars = []
        L = len(self.tokens)
        for i in range(0, L):
            item = self.tokens[i]
            if item.type_ == TVAR and not item.index_ in vars:
                vars.append(item.index_)
        return vars


class Parser():

    PRIMARY      = 1
    OPERATOR     = 2
    FUNCTION     = 4
    LPAREN       = 8
    RPAREN       = 16
    COMMA        = 32
    SIGN         = 64
    CALL         = 128
    NULLARY_CALL = 256

    def neg(self, a):
        return -a

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        return a / b


    def __init__(self):
        self.success = False
        self.errormsg = ""
        self.expression = ""

        self.pos = 0

        self.tokennumber = 0
        self.tokenprio = 0
        self.tokenindex = 0
        self.tmpprio = 0

        self.ops1 = {
            "sqrt": math.sqrt,
            "log": math.log,
            "abs": abs,
            "-": self.neg
        }

        self.ops2 = {
            "+": self.add,
            "-": self.sub,
            "*": self.mul,
            '/': self.div,
            '^': math.pow
        }

        self.functions = {
            "pow": math.pow
        }

        self.consts = {
            'E': math.e,
            'PI': math.pi
        }

        self.values = {
            "sqrt": math.sqrt,
            "log": math.log,
            "abs": abs,
            "exp": math.exp,
            "pow": math.pow,
            "E": math.e,
            "PI": math.pi
        }

    def isOperator(self):
        ops = (
            ("+", 2, "+"),
            ("-", 2, "-"),
            ("*", 3, "*"),
            ("/", 4, "/"),
            ("^", 6, "^")
        )
        for token, priority, index in ops:
            if self.expression.startswith(token, self.pos):
                self.tokenprio = priority
                self.tokenindex = index
                self.pos += len(token)
                return True
        return False

    def isSign(self):
        code = self.expression[self.pos - 1]
        return (code == '+') or (code == '-')

    def isPositiveSign(self):
        code = self.expression[self.pos - 1]
        return code == '+'

    def isNegativeSign(self):
        code = self.expression[self.pos - 1]
        return code == '-'

    def isLeftParenth(self):
        code = self.expression[self.pos]
        if code == '(':
            self.pos += 1
            self.tmpprio += 10
            return True
        return False

    def isRightParenth(self):
        code = self.expression[self.pos]
        if code == ')':
            self.pos += 1
            self.tmpprio -= 10
            return True
        return False

    def isComma(self):
        code = self.expression[self.pos]
        if code==',':
            self.pos+=1
            self.tokenprio=-1
            self.tokenindex=","
            return True
        return False

    def isWhite(self):
        code = self.expression[self.pos]
        if code.isspace():
            self.pos += 1
            return True
        return False

    def isOp1(self):
        str = ''
        for i in range(self.pos, len(self.expression)):
            c = self.expression[i]
            if c.upper() == c.lower():
                if i == self.pos or (c != '_' and (c < '0' or c > '9')):
                    break
            str += c
        if len(str) > 0 and str in self.ops1:
            self.tokenindex = str
            self.tokenprio = 7
            self.pos += len(str)
            return True
        return False

    def isOp2(self):
        str = ''
        for i in range(self.pos, len(self.expression)):
            c = self.expression[i]
            if c.upper() == c.lower():
                if i == self.pos or (c != '_' and (c < '0' or c > '9')):
                    break
            str += c
        if len(str) > 0 and (str in self.ops2):
            self.tokenindex = str
            self.tokenprio = 7
            self.pos += len(str)
            return True
        return False

    def isVar(self):
        str = ""
        inQuotes = False
        for i in range(self.pos, len(self.expression)):
            c = self.expression[i]
            if c.lower() == c.upper():
                if ((i == self.pos and c != "\"") or (not (c in "_.\"") and (c < "0" or c > "9"))) and not inQuotes:
                    break
            if c == "\"":
                inQuotes = not inQuotes
            str += c
        if str:
            self.tokenindex = str
            self.tokenprio = 4
            self.pos += len(str)
            return True
        return False

    def addfunc(self, tokenstack, operstack, type_):
        operator = Token(
            type_,
            self.tokenindex,
            self.tokenprio + self.tmpprio,
            0,
        )
        while len(operstack) > 0:
            if operator.prio_ <= operstack[len(operstack) - 1].prio_:
                tokenstack.append(operstack.pop())
            else:
                break
        operstack.append(operator)

    def error_parsing(self, column, msg):
        self.success = False
        self.errormsg = "parse error [column " + str(column) + "]: " + msg
        raise Exception(self.errormsg)

    def isNumber(self):
        r = False
        str = ""
        while self.pos < len(self.expression):
            code = self.expression[self.pos]
            if (code >= "0" and code <= "9") or code == ".":
                str += self.expression[self.pos]
                self.pos += 1
                self.tokennumber = float(str)
                r = True
            else:
                break
        return r

    def isString(self):
        r = False
        str = ""
        startpos = self.pos
        if self.pos < len(self.expression) and self.expression[self.pos] == "'":
            self.pos += 1
            while self.pos < len(self.expression):
                code = self.expression[self.pos]
                if code != "\"" or (str != "" and str[-1] == "\\"):
                    str += self.expression[self.pos]
                    self.pos += 1
                else:
                    self.pos += 1
                    self.tokennumber = self.unescape(str, startpos)
                    r = True
                    break
        return r

    def isConst(self):
        for i in self.consts:
            L = len(i)
            str = self.expression[self.pos:self.pos + L]
            if i == str:
                if len(self.expression) <= self.pos + L:
                    self.tokennumber = self.consts[i]
                    self.pos += L
                    return True
                if not self.expression[self.pos + L].isalnum() and self.expression[self.pos + L] != "_":
                    self.tokennumber = self.consts[i]
                    self.pos += L
                    return True
        return False

    def parse(self, expr):
        self.errormsg = ""
        self.success = True
        operstack = []
        tokenstack = []
        self.tmpprio = 0
        expected = self.PRIMARY | self.LPAREN | self.FUNCTION | self.SIGN
        noperators = 0
        self.expression = expr
        self.pos = 0

        while self.pos < len(self.expression):
            if self.isOperator():
                if self.isSign() and expected & self.SIGN:
                    if self.isNegativeSign():
                        self.tokenprio = 5
                        self.tokenindex = "-"
                        noperators += 1
                        self.addfunc(tokenstack, operstack, TOP1)
                    expected = self.PRIMARY | self.LPAREN | self.FUNCTION | self.SIGN
                if (expected & self.OPERATOR) == 0:
                    self.error_parsing(self.pos, "unexpected operator")
                noperators += 2
                self.addfunc(tokenstack, operstack, TOP2)
                expected = self.PRIMARY | self.LPAREN | self.FUNCTION | self.SIGN

            elif self.isNumber():
                if (expected & self.PRIMARY) == 0:
                    self.error_parsing(self.pos, "unexpected number")
                token = Token(TNUMBER, 0, 0, self.tokennumber)
                tokenstack.append(token)
                expected = self.OPERATOR | self.RPAREN | self.COMMA

            elif self.isString():
                if (expected & self.PRIMARY) == 0:
                    self.error_parsing(self.pos, "unexpected string")
                token = Token(TNUMBER, 0, 0, self.tokennumber)
                tokenstack.append(token)
                expected = self.OPERATOR | self.RPAREN | self.COMMA

            elif self.isLeftParenth():
                if (expected & self.LPAREN) == 0:
                    self.error_parsing(self.pos, "unexpected \"(\"")
                if expected and self.CALL:
                    noperators += 2
                    self.tokenprio = -2
                    self.tokenindex = -1
                    self.addfunc(tokenstack, operstack, TFUNCALL)
                    expected = self.PRIMARY | self.LPAREN | self.FUNCTION | self.SIGN | self.NULLARY_CALL

            elif self.isRightParenth():
                if (expected & self.RPAREN) == 0:
                    self.error_parsing(self.pos, "unexpected \")\"")
                expected = self.OPERATOR | self.RPAREN | self.COMMA | self.LPAREN | self.CALL
                if expected and self.NULLARY_CALL:
                    token = Token(TNUMBER, 0, 0, [])
                tokenstack.append(token)

            elif self.isConst():
                if (expected & self.PRIMARY) == 0:
                    self.error_parsing(self.pos, "unexpected constant")
                token = Token(TNUMBER, 0, 0, self.tokennumber)
                tokenstack.append(token)
                expected = self.OPERATOR | self.RPAREN | self.COMMA

            elif self.isOp2():
                if (expected & self.FUNCTION) == 0:
                    self.error_parsing(self.pos, "unexpected function operator")
                self.addfunc(tokenstack, operstack, TOP2)
                noperators += 1
                expected = self.LPAREN

            elif self.isOp1():
                if (expected & self.FUNCTION) == 0:
                    self.error_parsing(self.pos, "unexpected function operator")
                self.addfunc(tokenstack, operstack, TOP1)
                noperators += 1
                expected = self.LPAREN

            elif self.isVar():
                if (expected & self.PRIMARY) == 0:
                    self.error_parsing(self.pos, "unexpected variable")
                vartoken = Token(TVAR, self.tokenindex, 0, 0)
                tokenstack.append(vartoken)
                expected = self.OPERATOR | self.RPAREN | self.COMMA | self.LPAREN | self.CALL

            elif self.isWhite():
                pass

            else:
                if self.errormsg == "":
                    self.error_parsing(self.pos, "unknown character")
                else:
                    self.error_parsing(self.pos, self.errormsg)

        while len(operstack) > 0:
            op = operstack.pop()
            tokenstack.append(op)

        return Expression(tokenstack, self.ops1, self.ops2, self.functions)

    def evaluate(self, expr, variables):
        return self.parse(expr).evaluate(variables)