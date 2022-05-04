from enum import IntEnum
class TokenType(IntEnum):
    eof = 0
    Tok_lparen = 1
    Tok_rparen = 2
    Tok_mul = 3
    Tok_plus = 4
    Tok_comma = 5
    Tok_minus = 6
    Tok_del = 7
    Tok_doublep = 8
    Tok_semicol = 9
    Tok_assign = 10
    Tok_pow = 11
    Tok_id = 12
    Tok_int = 13
    Tok_float = 14
    Tok_let = 15
    Tok_typeInt = 16
    Tok_func = 17
    Tok_typeFloat = 18
    Tok_typeFun = 19

class Buf:
    def __init__(self, it):
        self.current = iter(it)
        self.stack = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration
        try:
            return next(self.current)
        except StopIteration:
            if self.stack:
                self.current = self.stack.pop()
                return next(self)
            else:
                self.current = None
                raise StopIteration

    def __bool__(self):
        return self.current is not None

    def unshift(self, it):
        self.stack.append(self.current)
        self.current = iter(it)



def lex(input, debug = False):
    inputBuf = Buf(input)

    while True:
        curCh = None
        accSt = -1
        curSt = 0
        buf = ""
        tmp = ""
        while curSt >= 0:
            if curSt in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,21,22,23,24,25,26,27,28,29,30,31,32,33]:
                buf += tmp
                tmp = ""
                accSt = curSt
            if curSt in []:
                break
            try:
                curCh = next(inputBuf)
            except StopIteration:
                break
            tmp += curCh
            if curSt == 0:
                if curCh == '\U00000009' or curCh == '\U0000000a' or curCh == ' ':
                    curSt = 1
                    continue
                elif curCh == '(':
                    curSt = 2
                    continue
                elif curCh == ')':
                    curSt = 3
                    continue
                elif curCh == '*':
                    curSt = 4
                    continue
                elif curCh == '+':
                    curSt = 5
                    continue
                elif curCh == ',':
                    curSt = 6
                    continue
                elif curCh == '-':
                    curSt = 7
                    continue
                elif curCh == '/':
                    curSt = 8
                    continue
                elif curCh == ':':
                    curSt = 9
                    continue
                elif curCh == ';':
                    curSt = 10
                    continue
                elif curCh == '=':
                    curSt = 11
                    continue
                elif curCh == '^':
                    curSt = 12
                    continue
                elif curCh == 'f':
                    curSt = 14
                    continue
                elif curCh == 'i':
                    curSt = 15
                    continue
                elif curCh == 'l':
                    curSt = 16
                    continue
                elif curCh == '_' or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                elif (curCh >= '0' and curCh <= '9'):
                    curSt = 17
                    continue
                break
            elif curSt == 1:
                if curCh == '\U00000009' or curCh == '\U0000000a' or curCh == ' ':
                    curSt = 1
                    continue
                break
            elif curSt == 7:
                if curCh == '>':
                    curSt = 33
                    continue
                break
            elif curSt == 13:
                if curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 14:
                if curCh == 'l':
                    curSt = 26
                    continue
                elif curCh == 'u':
                    curSt = 27
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 15:
                if curCh == 'n':
                    curSt = 24
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 16:
                if curCh == 'e':
                    curSt = 22
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 17:
                if curCh == '.':
                    curSt = 18
                    continue
                elif curCh == 'E' or curCh == 'e':
                    curSt = 19
                    continue
                elif (curCh >= '0' and curCh <= '9'):
                    curSt = 17
                    continue
                break
            elif curSt == 18:
                if curCh == 'E' or curCh == 'e':
                    curSt = 19
                    continue
                elif (curCh >= '0' and curCh <= '9'):
                    curSt = 18
                    continue
                break
            elif curSt == 19:
                if curCh == '+' or curCh == '-':
                    curSt = 20
                    continue
                elif (curCh >= '0' and curCh <= '9'):
                    curSt = 21
                    continue
                break
            elif curSt == 20:
                if (curCh >= '0' and curCh <= '9'):
                    curSt = 21
                    continue
                break
            elif curSt == 21:
                if (curCh >= '0' and curCh <= '9'):
                    curSt = 21
                    continue
                break
            elif curSt == 22:
                if curCh == 't':
                    curSt = 23
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 23:
                if curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 24:
                if curCh == 't':
                    curSt = 25
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 25:
                if curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 26:
                if curCh == 'o':
                    curSt = 30
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 27:
                if curCh == 'n':
                    curSt = 28
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 28:
                if curCh == 'c':
                    curSt = 29
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 29:
                if curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 30:
                if curCh == 'a':
                    curSt = 31
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 31:
                if curCh == 't':
                    curSt = 32
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            elif curSt == 32:
                if curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 13
                    continue
                break
            break

        if tmp:
            inputBuf.unshift(tmp)
        text = buf
        if accSt == 1:
            if debug: print("Skipping state 1: \"" + text + "\"")
            continue
        elif accSt == 2:
            if debug: print("Lexed token lparen: \"" + text + "\"")
            yield (TokenType.Tok_lparen, None)
            continue
        elif accSt == 3:
            if debug: print("Lexed token rparen: \"" + text + "\"")
            yield (TokenType.Tok_rparen, None)
            continue
        elif accSt == 4:
            if debug: print("Lexed token mul: \"" + text + "\"")
            yield (TokenType.Tok_mul, None)
            continue
        elif accSt == 5:
            if debug: print("Lexed token plus: \"" + text + "\"")
            yield (TokenType.Tok_plus, None)
            continue
        elif accSt == 6:
            if debug: print("Lexed token comma: \"" + text + "\"")
            yield (TokenType.Tok_comma, None)
            continue
        elif accSt == 7:
            if debug: print("Lexed token minus: \"" + text + "\"")
            yield (TokenType.Tok_minus, None)
            continue
        elif accSt == 8:
            if debug: print("Lexed token del: \"" + text + "\"")
            yield (TokenType.Tok_del, None)
            continue
        elif accSt == 9:
            if debug: print("Lexed token doublep: \"" + text + "\"")
            yield (TokenType.Tok_doublep, None)
            continue
        elif accSt == 10:
            if debug: print("Lexed token semicol: \"" + text + "\"")
            yield (TokenType.Tok_semicol, None)
            continue
        elif accSt == 11:
            if debug: print("Lexed token assign: \"" + text + "\"")
            yield (TokenType.Tok_assign, None)
            continue
        elif accSt == 12:
            if debug: print("Lexed token pow: \"" + text + "\"")
            yield (TokenType.Tok_pow, None)
            continue
        elif accSt == 13:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 14:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 15:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 16:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 17:
            if debug: print("Lexed token int: \"" + text + "\"")
            yield (TokenType.Tok_int,  int(text) )
            continue
        elif accSt == 18:
            if debug: print("Lexed token float: \"" + text + "\"")
            yield (TokenType.Tok_float,  float(text) )
            continue
        elif accSt == 21:
            if debug: print("Lexed token float: \"" + text + "\"")
            yield (TokenType.Tok_float,  float(text) )
            continue
        elif accSt == 22:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 23:
            if debug: print("Lexed token let: \"" + text + "\"")
            yield (TokenType.Tok_let, None)
            continue
        elif accSt == 24:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 25:
            if debug: print("Lexed token typeInt: \"" + text + "\"")
            yield (TokenType.Tok_typeInt, None)
            continue
        elif accSt == 26:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 27:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 28:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 29:
            if debug: print("Lexed token func: \"" + text + "\"")
            yield (TokenType.Tok_func, None)
            continue
        elif accSt == 30:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 31:
            if debug: print("Lexed token id: \"" + text + "\"")
            yield (TokenType.Tok_id, text)
            continue
        elif accSt == 32:
            if debug: print("Lexed token typeFloat: \"" + text + "\"")
            yield (TokenType.Tok_typeFloat, None)
            continue
        elif accSt == 33:
            if debug: print("Lexed token typeFun: \"" + text + "\"")
            yield (TokenType.Tok_typeFun, None)
            continue
        if not inputBuf:
            if debug: print("Got EOF while lexing \"" + text + "\"")
            yield (TokenType.eof, None)
            continue
        raise Exception("Unexpected input: " + buf + tmp)