import copy

objects={}

class IntType:
    def __repr__(self):
        return "int"
    def coercible(self, other):
        return isinstance(other, FloatType) or isinstance(other, IntType)

class FloatType:
    def __repr__(self):
        return "float"
    def coercible(self, other):
        return isinstance(other, FloatType)

class FunctionType:
    def __init__(self, args, result):
        self.args = args
        self.result = result
    def __repr__(self):
        args = ','.join(repr(x) for x in self.args)
        return f"({args}) -> {self.result}"
    def coercible(self, other):
        if isinstance(other, FunctionType):
            return all(y.coercible(x) for x, y in zip(self.args, other.args)) and self.result.coercible(other.result)
        else:
            return False

class Int:
    def __init__(self, tok):
        self.Value = tok
        self.Type = IntType()

    def __repr__(self):
        return f"({self.Value}, {self.Type})"

    def type(self, context):
        return self.Type

class Float:
    def __init__(self, tok):
        self.Value = tok
        self.Type = FloatType()

    def __repr__(self):
        return f"({self.Value}, {self.Type})"

    def type(self, context):
        return self.Type

class Id:
    def __init__(self, tok):
        self.Value = tok
    def __repr__(self):
        return f"{self.Value}"
    def type(self, context):
        t = context.get(self.Value)
        if t is None:
            raise Exception(f"Unknown variable {self.Value}")
        return t


class Param:
    def __init__(self, tok, type):
        self.Value = tok
        self.Type = type

    def __repr__(self):
        return f"({self.Value}, {self.Type})"

    def type(self, context):
        return self.Type

class UnaryOp:
    def __init__(self, tok, branch):
        self.Value = tok
        self.Branch = branch
    def __repr__(self):
        return f"({self.Value}, {self.Branch})"
    def type(self, context):
        return self.Branch.type(context)

class BinaryOp:
    def __init__(self, tok, branchl, branchr):
        self.Value = tok
        self.BranchL = branchl
        self.BranchR = branchr

    def __repr__(self):
        return f"({self.Value}, {self.BranchL}, {self.BranchR})"

    def type(self, context):
        if (self.BranchL.type(context).coercible(self.BranchR.type(context))):
            return self.BranchR.type(context)
        elif (self.BranchR.type(context).coercible(self.BranchL.type(context))):
            return self.BranchR.type(context)
        else:
            raise Exception(f"Non-coercible types for binop {self.Value}: {self.BranchL.type(context)} and {self.BranchR.type(context)}")

class Call:
    def __init__(self, tok, args):
        self.Value = tok
        self.Args = args
    def __repr__(self):
        return f"({self.Value}, {self.Args})"

    def type(self, context):
        argsType = [x.type(context) for x in self.Args]
        func = context.get(self.Value)

        if not isinstance(func, FunctionType):
            raise Exception(f"Expected function, got {func}")

        if len(argsType) != len(func.args):
            raise Exception(f"Expected {len(func.args)} arguments, but got {len(argsType)}")

        if not all(x.coercible(y) for x, y in zip(argsType, func.args)):
            raise Exception(f"Non-coercible types {argsType}, {func.args}")

        return func.result


class Assign:
    def __init__(self, tok, expr):
        self.Value = tok
        self.Expr = expr
    def __repr__(self):
        return f"({self.Value}, {self.Expr})"

    def type(self, context):
        return self.Expr.type(context)

class Function:
    def __init__(self, tok, args, expr):
        self.Value = tok
        self.Args = args
        self.Expr = expr
    def __repr__(self):
        return f"({self.Value}, {self.Args}, {self.Expr})"
    def type(self, context):
        localContext = dict(**context)
        localContext.update({ f.Value: f.Type for f in self.Args })
        return FunctionType([arg.Type for arg in self.Args], self.Expr.type(localContext))

def make(f, *args):
    t = objects.get((f, *args))
    if t is  None:
        t = f(*args)
        objects[(f, *args)] = t
    return t

def clearObjects(arg):
    objects.clear()
    return arg