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
        self.number_ = number_ if number_ !=None else 0

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

                nstack.append(frm.format(n1=n1,n2=n2,f=f))
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






# class Parser():
