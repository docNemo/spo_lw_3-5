import parser
import lexer
from parser import Parser

lexer = lexer.Lexer("func asdf(id1:int, id3:int, id4:float) = id1 + id3 - id4");
# lexer = lexer.Lexer("3+3.0 * 3 ^ (-3.0)");
# lexer = lexer.Lexer("asdf(id1, 4, id3, id4)");
parser = parser.Parser(lexer);
print(parser.parse());
