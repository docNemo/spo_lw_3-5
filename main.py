from posixpath import split
from parser import *
from lexer import *

input = ''' func f(a1:int) = a1 * a1
            func ads(a1:float, a2:float, a3:int) = a1 + f(a2) * a3
            let a1 = 3.0
            let a2 = 3.0
            let a3 = 4
            let a4 = 4 + 4
            ads(a1, a2, a3)'''

for b in input.split('\n'):
    lexer = Lexer(b)
    parser = Parser(lexer)
    tree = parser.parse()

print(tree)
print(tree.type())