class Literal:
    def __init__(self, tok, type):
        self.Value = tok
        self.Type = type

    def __repr__(self):
        return f"({self.Value}, {self.Type})"

    def type(self):
        return self.Type

class Id:
    def __init__(self, tok):
        self.Value = tok
    def __repr__(self):
        return f"{self.Value}"

class Param:
    def __init__(self, tok, type):
        self.Value = tok
        self.Type = type

    def __repr__(self):
        return f"({self.Value}, {self.Type})"

    def type(self):
        return self.Type

class UnaryOp:
    def __init__(self, tok, branch):
        self.Value = tok
        self.Branch = branch
    def __repr__(self):
        return f"({self.Value}, {self.Branch})"
    def type(self):
        return self.Branch.type()

class BinaryOp:
    def __init__(self, tok, branchl, branchr):
        self.Value = tok
        self.BranchL = branchl
        self.BranchR = branchr

    def __repr__(self):
        return f"({self.Value}, {self.BranchL}, {self.BranchR})"

    def type(self):
        if (self.BranchL.type() == "float" or self.BranchR.type() == "float"):
            return "float"
        else:
            return "int"

class Call:
    def __init__(self, tok, args):
        self.Value = tok
        self.Args = args
    def __repr__(self):
        return f"({self.Value}, {self.Args}, {functions.get(self.Value).Expr} )"
    
    def type(self):
        argsType = [x.type() for x in self.Args]
        func = functions.get(self.Value)
        
        for a, f in zip(argsType, func.Args):
            if (f.type() == "int") and (a == "float"):
                exit(f"Встречен float, когда ожидался int аргумента {f.Value} функции {self.Value}")
        
        return func.Expr.type()
         

class Assign:
    def __init__(self, tok, expr):
        self.Value = tok
        self.Expr = expr
    def __repr__(self):
        return f"({self.Value}, {self.Expr})"

    def type(self):
        return self.Expr.type()

class Function:
    def __init__(self, tok, args, expr):
        self.Value = tok
        self.Args = args
        self.Expr = expr
    def __repr__(self):
        return f"({self.Value}, {self.Args}, {self.Expr})"
    def type(self):
        return self.Expr.type() 


functions = {}
functionArgs = {}
objects = {}

def make(f, *args):
        t = objects.get((f, *args))
        if t is  None:
            t = f(*args)
            objects[(f, *args)] = t
        return t

def makeId(f, name, *args):
        t = objects.get(name)
        if t is None:
            t = f(name, *args)
            objects[name] = t
        return t

def makeF(f, args, expr):
        t = functions.get(f)
        if t is None:
            functions[f] = Function(f, args, expr)
        
        functionArgs.clear()
        return Function(f, args, expr)

def makeFArgs(f,name, *args):
        t = functionArgs.get(name)
        if t is None:
            t = f(name, *args)
            functionArgs[name] = t
        else:
            exit(f"Повторяющийся аргумент функции {name}")
        return t

def makeFBody(f, *args):
        t = functionArgs.get((f, *args))
        if t is  None:
            t = f(*args)
            functionArgs[(f, *args)] = t
        return t

def makeFBodyParam(f,name):
        t = functionArgs.get(name)
        if t is  None:
            exit(f"Неопределенный идентифкатор {f}")
        return t

def beginArgs(t):
    functionArgs.clear()
    return t

def makeC(f, name, args):
        t = functions.get(name)
        if t is None:
            exit(f"Неизвестная функция {f}")
        return f(name, args)






