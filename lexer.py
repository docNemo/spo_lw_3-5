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
    Tok_assign = 9
    Tok_pow = 10
    Tok_id = 11
    Tok_int = 12
    Tok_float = 13
    Tok_let = 14
    Tok_type = 15
    Tok_func = 16

class Lexer:
    def __init__(self, input, debug = False):
        self.input = input
        self.curChIx = 0
        self.debug = debug

    def getNextToken(self):
        lastAccChIx = self.curChIx
        startChIx = self.curChIx
        curCh = '\0'
        accSt = -1
        curSt = 0
        while curSt >= 0:
            if curSt in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,20,21,22,23,24,25,26,27,28,29,30]:
                lastAccChIx = self.curChIx
                accSt = curSt
            if curSt in []:
                break
            if self.curChIx >= len(self.input): break
            curCh = self.input[self.curChIx]
            self.curChIx+=1
            if curSt == 0:
                if curCh == ' ':
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
                elif curCh == '=':
                    curSt = 10
                    continue
                elif curCh == '^':
                    curSt = 11
                    continue
                elif curCh == 'f':
                    curSt = 13
                    continue
                elif curCh == 'i':
                    curSt = 14
                    continue
                elif curCh == 'l':
                    curSt = 15
                    continue
                elif curCh == '_' or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                elif (curCh >= '0' and curCh <= '9'):
                    curSt = 16
                    continue
                break
            elif curSt == 1:
                if curCh == ' ':
                    curSt = 1
                    continue
                break
            elif curSt == 12:
                if curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 13:
                if curCh == 'l':
                    curSt = 25
                    continue
                elif curCh == 'u':
                    curSt = 26
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 14:
                if curCh == 'n':
                    curSt = 23
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 15:
                if curCh == 'e':
                    curSt = 21
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 16:
                if curCh == '.':
                    curSt = 17
                    continue
                elif curCh == 'E' or curCh == 'e':
                    curSt = 18
                    continue
                elif (curCh >= '0' and curCh <= '9'):
                    curSt = 16
                    continue
                break
            elif curSt == 17:
                if curCh == 'E' or curCh == 'e':
                    curSt = 18
                    continue
                elif (curCh >= '0' and curCh <= '9'):
                    curSt = 17
                    continue
                break
            elif curSt == 18:
                if curCh == '+' or curCh == '-':
                    curSt = 19
                    continue
                elif (curCh >= '0' and curCh <= '9'):
                    curSt = 20
                    continue
                break
            elif curSt == 19:
                if (curCh >= '0' and curCh <= '9'):
                    curSt = 20
                    continue
                break
            elif curSt == 20:
                if (curCh >= '0' and curCh <= '9'):
                    curSt = 20
                    continue
                break
            elif curSt == 21:
                if curCh == 't':
                    curSt = 22
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 22:
                if curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 23:
                if curCh == 't':
                    curSt = 24
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 24:
                if curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 25:
                if curCh == 'o':
                    curSt = 29
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 26:
                if curCh == 'n':
                    curSt = 27
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 27:
                if curCh == 'c':
                    curSt = 28
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 28:
                if curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 29:
                if curCh == 'a':
                    curSt = 30
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            elif curSt == 30:
                if curCh == 't':
                    curSt = 24
                    continue
                elif curCh == '_' or (curCh >= '0' and curCh <= '9') or (curCh >= 'a' and curCh <= 'z'):
                    curSt = 12
                    continue
                break
            break

        lastReadChIx = self.curChIx
        self.curChIx = lastAccChIx
        text = self.input[startChIx:lastAccChIx]
        if accSt == 1:
            if self.debug: print("Skipping state 1: \"" + text + "\"")
            return self.getNextToken()
        elif accSt == 2:
            if self.debug: print("Lexed token lparen: \"" + text + "\"")
            return (TokenType.Tok_lparen, None)
        elif accSt == 3:
            if self.debug: print("Lexed token rparen: \"" + text + "\"")
            return (TokenType.Tok_rparen, None)
        elif accSt == 4:
            if self.debug: print("Lexed token mul: \"" + text + "\"")
            return (TokenType.Tok_mul, None)
        elif accSt == 5:
            if self.debug: print("Lexed token plus: \"" + text + "\"")
            return (TokenType.Tok_plus, None)
        elif accSt == 6:
            if self.debug: print("Lexed token comma: \"" + text + "\"")
            return (TokenType.Tok_comma, None)
        elif accSt == 7:
            if self.debug: print("Lexed token minus: \"" + text + "\"")
            return (TokenType.Tok_minus, None)
        elif accSt == 8:
            if self.debug: print("Lexed token del: \"" + text + "\"")
            return (TokenType.Tok_del, None)
        elif accSt == 9:
            if self.debug: print("Lexed token doublep: \"" + text + "\"")
            return (TokenType.Tok_doublep, None)
        elif accSt == 10:
            if self.debug: print("Lexed token assign: \"" + text + "\"")
            return (TokenType.Tok_assign, None)
        elif accSt == 11:
            if self.debug: print("Lexed token pow: \"" + text + "\"")
            return (TokenType.Tok_pow, None)
        elif accSt == 12:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        elif accSt == 13:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        elif accSt == 14:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        elif accSt == 15:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        elif accSt == 16:
            if self.debug: print("Lexed token int: \"" + text + "\"")
            return (TokenType.Tok_int,  int(text) )
        elif accSt == 17:
            if self.debug: print("Lexed token float: \"" + text + "\"")
            return (TokenType.Tok_float,  float(text) )
        elif accSt == 20:
            if self.debug: print("Lexed token float: \"" + text + "\"")
            return (TokenType.Tok_float,  float(text) )
        elif accSt == 21:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        elif accSt == 22:
            if self.debug: print("Lexed token let: \"" + text + "\"")
            return (TokenType.Tok_let, None)
        elif accSt == 23:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        elif accSt == 24:
            if self.debug: print("Lexed token type: \"" + text + "\"")
            return (TokenType.Tok_type, text)
        elif accSt == 25:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        elif accSt == 26:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        elif accSt == 27:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        elif accSt == 28:
            if self.debug: print("Lexed token func: \"" + text + "\"")
            return (TokenType.Tok_func, None)
        elif accSt == 29:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        elif accSt == 30:
            if self.debug: print("Lexed token id: \"" + text + "\"")
            return (TokenType.Tok_id, text)
        if self.curChIx >= len(self.input):
            if self.debug: print("Got EOF while lexing \"" + text + "\"")
            return (TokenType.eof, None)
        raise Exception("Unexpected input: " + self.input[startChIx:lastReadChIx])