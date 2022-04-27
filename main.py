from parser import *
from lexer import *

input = ''' let a1 = 3 * 4.0;
            func f(a1:int) = a1 * a1;
            let a2 = 4 * 3;
            func f1(a2:float) = a2 + f(1);
            f1(a1) * f(a2);
            a1 + 4;
            a2 + 4 ^ f1(a2);
            f(2)'''

lexer = Lexer(input)
parser = Parser(lexer)
trees = parser.parse()

print(trees)
for tree in trees:
    if (not isinstance(tree, Function)) and (not isinstance(tree, Assign)):
        print("\n###################################\n")
        print(tree)
        print(tree.type())