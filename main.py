from posixpath import split
from parser import *
from lexer import *

input = ''' let id4 = 4
            let id = -3
            let h = -3
            id4 + id ^ h'''

for b in input.split('\n'):
    lexer = Lexer(b)
    parser = Parser(lexer)
    tree = parser.parse()
# lexer = lexer.Lexer("func asdf(id1:int, id3:int, id4:float) = id1 + id3 - id4")
# lexer = lexer.Lexer("3+3.0 * 3 ^ (-3.0)");
# lexer = Lexer("id4 + id4")
# parser = Parser(lexer)
print(tree)
print(tree.type())
