import parser
import lexer
from parser import Parser

# lexer = lexer.Lexer("$func asdf(id1, id2, id3, id4) = id1 * id2 - id3 ^ id4");
parser = parser.Parser(lexer);
print(parser.parse());
