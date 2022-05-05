from classes import *

def getBinaryArg(tree, context, results):
    if isinstance(tree.L, Var_):
        arg1 = interp(context.get(tree.L.V), context)
    elif isinstance(tree.L, Int_) or isinstance(tree.L, Float_):
        arg1 = tree.L.V
    else:
        arg1 = results[tree.L]
        
    if isinstance(tree.R, Var_):
        arg2 = interp(context.get(tree.R.V), context)
    elif isinstance(tree.R, Int_) or isinstance(tree.R, Float_):
        arg2 = tree.R.V
    else:
        arg2 = results[tree.R]
    
    return [arg1, arg2]

class AddInt:    
    def __init__(self, l, r):
        self.L = l
        self.R = r

    def __repr__(self):
        return f"AddInt {self.L} {self.R}"

    def calc(self, context, result, *_):
        args = getBinaryArg(self, context, result)
        return args[0] + args[1]

class SubInt:    
    def __init__(self, l, r):
        self.L = l
        self.R = r

    def __repr__(self):
        return f"SubInt {self.L} {self.R}"
    
    def calc(self, context, result, *_):
        args = getBinaryArg(self, context, result)
        return args[0] - args[1]

class MulInt:    
    def __init__(self, l, r):
        self.L = l
        self.R = r

    def __repr__(self):
        return f"MulInt {self.L} {self.R}"
    
    def calc(self, context, result, *_):
        args = getBinaryArg(self, context, result)
        return args[0] * args[1]

class DivInt:    
    def __init__(self, l, r):
        self.L = l
        self.R = r

    def __repr__(self):
        return f"DivInt {self.L} {self.R}"

    def calc(self, context, result, *_):
        args = getBinaryArg(self, context, result)
        return args[0] // args[1]

class PowInt:    
    def __init__(self, l, r):
        self.L = l
        self.R = r
    def __repr__(self):
        return f"PowInt {self.L} {self.R}"

    def calc(self, context, result, *_):
        args = getBinaryArg(self, context, result)
        return args[0]** args[1]

class NegInt:    
    def __init__(self, v):
        self.V = v
    
    def __repr__(self):
        return f"NegInt {self.V}"

    def calc(self, context, result, *_):
        if isinstance(self.V, Var_):
            arg = interp(context.get(self.V))
        elif isinstance(self.V, Int_) or isinstance(self.V, Float_):
            arg = self.V.V
        else:
            arg = result[self.V]

        return -arg

class AddFloat:    
    def __init__(self, l, r):
        self.L = l
        self.R = r
    
    def __repr__(self):
        return f"AddFloat {self.L} {self.R}"

    def calc(self, context, result, *_):
        args = getBinaryArg(self, context, result)
        return args[0] + args[1]

class SubFloat:    
    def __init__(self, l, r):
        self.L = l
        self.R = r
    
    def __repr__(self):
        return f"SubFloat {self.L} {self.R}"

    def calc(self, context, result, *_):
        args = getBinaryArg(self, context, result)
        return args[0] - args[1]

class MulFloat:    
    def __init__(self, l, r):
        self.L = l
        self.R = r
    
    def __repr__(self):
        return f"MulFloat {self.L} {self.R}"

    def calc(self, context, result, *_):
        args = getBinaryArg(self, context, result)
        return args[0] * args[1]

class DivFloat:    
    def __init__(self, l, r):
        self.L = l
        self.R = r
    
    def __repr__(self):
        return f"DivFloat {self.L} {self.R}"

    def calc(self, context, result, *_):
        args = getBinaryArg(self, context, result)
        return args[0] / args[1]

class PowFloat:    
    def __init__(self, l, r):
        self.L = l
        self.R = r
    
    def __repr__(self):
        return f"PowFloat {self.L} {self.R}"

    def calc(self, context, result, *_):
        args = getBinaryArg(self, context, result)
        return args[0]** args[1]

class NegFloat:    
    def __init__(self, v):
        self.V = v
    
    def __repr__(self):
        return f"NegFloat {self.V}"
    
    def calc(self, context, result, *_):
        if isinstance(self.V, Var_):
            arg = interp(context.get(self.V))
        elif isinstance(self.V, Int_) or isinstance(self.V, Float_):
            arg = self.V.V
        else:
            arg = result[self.V]

        return -arg

class IntToFloat:    
    def __init__(self, v):
        self.V = v

    def __repr__(self):
        return f"IntToFloat {self.V}"

    def calc(self, context, result, *_):
        if isinstance(self.V, Var_):
            arg = interp(context.get(self.V))
        elif isinstance(self.V, Int_) or isinstance(self.V, Float_):
            arg = self.V.V
        else:
            arg = result[self.V]
        return float(arg)

class Calls:
    def __init__(self, s, l):
        self.S = s
        self.L = l
    
    def __repr__(self):
        return f"Call {self.S} {self.L}"

    def calc(self, context, result, *a):
        args = []
        for a in self.L:
            if isinstance(a, Var_):
                args = args + [interp(context.get(a.V), context)]
            elif isinstance(a, Int_) or isinstance(a, Float_):
                args = args + [a.V]
            else:
                args = args + [result[a]]
        code = context.get(self.S)

        return interpF(code, args, context)

class Return:
    def __init__(self, w, n):
        self.W = w
        self.N = n
    
    def __repr__(self):
        return f"Return {self.W} {self.N}"

    def calc(self, context, result, *args):
        if isinstance(self.W, Int_) or isinstance(self.W, Float_):
            arg = self.W.V
        else:
            arg = result[self.W]
        return arg

class GetParam:
    def __init__(self, n):
        self.N = n
    
    def __repr__(self):
        return f"GetParam {self.N}"

    def calc(self, context, result, *args):
        return args[0][self.N]

class Exit:
    def __init__(self, w):
        self.W = w
    
    def __repr__(self):
        return f"Exit {self.W}"
    
    def calc(self, context, result, *_):
        if isinstance(self.W, Var_):
            arg = interp(context.get(self.W.V), context)
        elif isinstance(self.W, Int_) or isinstance(self.W, Float_):
            arg = self.W.V
        else:
            arg = result[self.W]
        return arg

class Var_:
    def __init__(self, w):
        self.V = w
    
    def __repr__(self):
        return f"Var {self.V}"
class Int_:
    def __init__(self, w):
        self.V = w
    
    def __repr__(self):
        return f"Int {self.V}"

class Float_:
    def __init__(self, w):
        self.V = w
    
    def __repr__(self):
        return f"Float {self.V}"

def getBinaryOpInt(op, l, r):
    if op == "+":
        return AddInt(l, r)
    if op == "-":
        return SubInt(l, r)
    if op == "*":
        return MulInt(l, r)
    if op == "/":
        return DivInt(l, r)
    if op == "^":
        return PowInt(l, r)

def getBinaryOpFloat(op, l, r):
    if op == "+":
        return AddFloat(l, r)
    if op == "-":
        return SubFloat(l, r)
    if op == "*":
        return MulFloat(l, r)
    if op == "/":
        return DivFloat(l, r)
    if op == "^":
        return PowFloat(l, r)

def getProgram(tree, context):
    if isinstance(tree, Id):
        return [Exit(Var_(tree.Value))]
    elif isinstance(tree, Int):
        return [Exit(Int_(tree.Value))]
    elif isinstance(tree, Int):
        return [Exit(Float_(tree.Value))]
    else:
        code = get3Code(tree, context, [])
        return code + [Exit(len(code) - 1)]

def get3Code(tree, context, code):
    if isinstance(tree, BinaryOp):
        if isinstance(tree.BranchL, Id):
            arg1 = Var_(tree.BranchL.Value)
        elif isinstance(tree.BranchL, Int):
            arg1 = Int_(tree.BranchL.Value)
        elif isinstance(tree.BranchL, Float):
            arg1 = Float_(tree.BranchL.Value)
        else:            
            code = get3Code(tree.BranchL, context, code)
            arg1 = len(code) - 1

        if isinstance(tree.BranchR, Id):
            arg2 = Var_(tree.BranchR.Value)
        elif isinstance(tree.BranchR, Int):
            arg2 = Int_(tree.BranchR.Value)
        elif isinstance(tree.BranchR, Float):
            arg2 = Float_(tree.BranchR.Value)
        else:            
            code = get3Code(tree.BranchR, context, code)
            arg2 = len(code) - 1

        if tree.BranchL.type(context).coercible(IntType()):
            if tree.BranchR.type(context).coercible(IntType()):
                code = code + [getBinaryOpInt(tree.Value, arg1, arg2)]
            else:
                code = code + [IntToFloat(arg1)]
                arg1 = len(code) - 1
                code = code + [getBinaryOpFloat(tree.Value, arg1, arg2)]
        else:
            if tree.BranchR.type(context).coercible(IntType()):
                code = code + [IntToFloat(arg2)]
                arg2 = len(code) - 1
                code = code + [getBinaryOpFloat(tree.Value, arg1, arg2)]
            else:
                code = code + [getBinaryOpFloat(tree.Value, arg1, arg2)]

    if isinstance(tree, UnaryOp):
        if isinstance(tree.Branch, Id):
            arg = Var_(tree.Branch.Value)
        elif isinstance(tree.Branch, Int):
            arg = Int_(tree.Branch.Value)
        elif isinstance(tree.Branch, Float):
            arg = Float_(tree.Branch.Value)
        else:            
            code = get3Code(tree.Branch, context, code)
            arg = len(code) - 1

        if tree.Branch.type(context).coercible(IntType()):
            code = code + [NegInt(arg)]
        else:
            code = code + [NegFloat(arg)]

    if isinstance(tree, Call): 
        args = []       
        for a in tree.Args:
            if isinstance(a, Id):
                arg = Var_(a.Value)
            elif isinstance(a, Int):
                arg = Int_(a.Value)
            elif isinstance(a, Float):
                arg = Float_(a.Value)
            else:            
                code = code + get3Code(a, context, code)
                arg = len(code) - 1
            args = args + [arg]
        code = code + [Calls(tree.Value, args)]
    return code

def getFCode(func, context):
    tree = func.Expr

    for t in func.Args:
        context[t.Value] = t.type(context)

    ARGS = [x.Value for x in func.Args]
    code = []

    if isinstance(tree, Id):
        return [GetParam(ARGS.index(tree.Value)), Return(0, len(ARGS))]
    elif isinstance(tree, Int):
        return [Return(Int_(tree.Value), len(ARGS))]
    elif isinstance(tree, Float):
        return [Return(Float_(tree.Value), len(ARGS))]
    else:
        code = getFuncCode(tree, context, ARGS, code)
        return code + [Return(len(code) - 1, len(ARGS))]

def getFuncCode(tree, context, ARGS, code):
    if isinstance(tree, BinaryOp):
        if isinstance(tree.BranchL, Id):
            code = code + [GetParam(ARGS.index(tree.BranchL.Value))]
            arg1 = len(code) - 1
        elif isinstance(tree.BranchL, Int):
            arg1 = Int_(tree.BranchL.Value)
        elif isinstance(tree.BranchL, Float):
            arg1 = Float_(tree.BranchL.Value)
        else:            
            code = getFuncCode(tree.BranchL, context, ARGS, code)
            arg1 = len(code) - 1

        if isinstance(tree.BranchR, Id):
            code = code + [GetParam(ARGS.index(tree.BranchR.Value))]
            arg2 = len(code) - 1
        elif isinstance(tree.BranchR, Int):
            arg2 = Int_(tree.BranchR.Value)
        elif isinstance(tree.BranchR, Float):
            arg2 = Float_(tree.BranchR.Value)
        else:            
            code = getFuncCode(tree.BranchR, context, ARGS, code)
            arg2 = len(code) - 1

        if tree.BranchL.type(context).coercible(IntType()):
            if tree.BranchR.type(context).coercible(IntType()):
                code = code + [getBinaryOpInt(tree.Value, arg1, arg2)]
            else:
                code = code + [IntToFloat(arg1)]
                arg1 = len(code) - 1
                code = code + [getBinaryOpFloat(tree.Value, arg1, arg2)]
        else:
            if tree.BranchR.type(context).coercible(IntType()):
                code = code + [IntToFloat(arg2)]
                arg2 = len(code) - 1
                code = code + [getBinaryOpFloat(tree.Value, arg1, arg2)]
            else:
                code = code + [getBinaryOpFloat(tree.Value, arg1, arg2)]

    if isinstance(tree, UnaryOp):
        if isinstance(tree.Branch, Id):
            code = code + [GetParam(ARGS.index(tree.Value))]
            arg = len(code) - 1
        elif isinstance(tree.Branch, Int):
            arg = Int_(tree.Branch.Value)
        elif isinstance(tree.Branch, Float):
            arg = Float_(tree.Branch.Value)
        else:            
            code = getFuncCode(tree.Branch, context, ARGS, code)
            arg = len(code) - 1

        if tree.Branch.type(context).coercible(IntType()):
            code = code + [NegInt(arg)]
        else:
            code = code + [NegFloat(arg)]

    if isinstance(tree, Call): 
        args = []       
        for a in tree.Args:
            if isinstance(a, Id):
                code = code + [GetParam(ARGS.index(a.Value))]
                arg = len(code) - 1
            elif isinstance(a, Int):
                 arg = Int_(a.Value)
            elif isinstance(a, Float):
                 arg = Float_(a.Value)
            else:            
                code = code + getFuncCode(a, context, ARGS, code)
                arg = len(code) - 1
            args = args + [arg]
        code = code + [Calls(tree.Value, args)]
    return code


def interp(code, context):
    result = []
    for c in code:
        result = result + [c.calc(context, result)]
    return result[-1]

def interpF(code, args, context):
    result = []
    for c in code:
        result = result + [c.calc(context, result, args)]
    return result[-1]