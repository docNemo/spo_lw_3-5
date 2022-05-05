from parser import *
from lexer import *
from get3Code import *

input = ''' let a1 = 3 * 4.0;
            func f(a1:int) = a1 * a1;
            let a2 = 4 * 3;
            func f1(a2:float) = a2 + f(1);
            f1(a1) * f(a2);
            a1 + 4;
            a2 + 4 ^ f1(a2);
            f(2);
            func f2(f:(float) -> float) = f(5);
            func f3() = 5;
            f3();
            2 + 2 * 2
            '''

parser = Parser()
trees = parser.parse(lex(input))

variables = {}
compileVar = {}

print(trees)
for tree in trees:
    if isinstance(tree, Function):
        variables[tree.Value] = tree.type(variables)
        compileVar[tree.Value] = getFCode(tree, variables)
    elif isinstance(tree, Assign):
        variables[tree.Value] = tree.type(variables)
        compileVar[tree.Value] = getProgram(tree.Expr, variables)
    else:
        print("\n###################################\n")
        print(tree)
        print(tree.type(variables))
        code = getProgram(tree, variables)
        print(code)
        print(interp(code, compileVar))