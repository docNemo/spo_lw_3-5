from lexer import *
from enum import IntEnum
from collections import deque


from classes import *


def stateToString(state):
  return [ ".","%eof","E","E","comma","Args1Call","doublep","id","type","comma","Args1","Args1","Args1Call","lparen","rparen","E","lparen","rparen","FBody","mul","E","E","E","E","E","E","E","plus","minus","del","pow","float","int","minus","id","lparen","rparen","ArgsCall","id","lparen","rparen","ArgsCall","assign","func","id","lparen","rparen","Args","FBody","mul","FBody","FBody","FBody","FBody","FBody","FBody","plus","minus","del","pow","float","int","minus","assign","id","let" ][state]

def expectedSym(state):
  return [ "E","%eof","%eof/mul/plus/minus/del/pow","rparen/comma/mul/plus/minus/del/pow","Args1Call","rparen","type/type","doublep/doublep","rparen/comma","Args1","rparen","rparen","rparen","E","%eof/comma/del/minus/mul/plus/pow/rparen","rparen/mul/plus/minus/del/pow","FBody","%eof/comma/del/minus/mul/plus/pow/rparen","rparen/mul/plus/minus/del/pow","E","mul/%eof/comma/del/minus/mul/plus/pow/rparen/plus/minus/del/pow","mul/plus/%eof/comma/del/minus/mul/plus/pow/rparen/minus/del/pow","mul/plus/minus/%eof/comma/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/del/%eof/comma/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","E","E","E","E","%eof/comma/del/minus/mul/plus/pow/rparen","%eof/comma/del/minus/mul/plus/pow/rparen","E","lparen/%eof/comma/del/minus/mul/plus/pow/rparen","ArgsCall","%eof/comma/del/minus/mul/plus/pow/rparen","rparen","lparen/%eof/comma/del/minus/mul/plus/pow/rparen","ArgsCall","%eof/comma/del/minus/mul/plus/pow/rparen","rparen","FBody","id","lparen","Args","assign","rparen","%eof/comma/del/minus/mul/plus/pow/rparen/mul/plus/minus/del/pow","FBody","mul/%eof/comma/del/minus/mul/plus/pow/rparen/plus/minus/del/pow","mul/plus/%eof/comma/del/minus/mul/plus/pow/rparen/minus/del/pow","mul/plus/minus/%eof/comma/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/del/%eof/comma/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","FBody","FBody","FBody","FBody","%eof/comma/del/minus/mul/plus/pow/rparen","%eof/comma/del/minus/mul/plus/pow/rparen","FBody","E","assign","id" ][state]

class Parser:
    Action = [
        [66,13,66,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [67,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66],
        [1,66,66,19,27,66,28,29,66,66,30,66,66,66,66,66,66],
        [66,66,68,19,27,4,28,29,66,66,30,66,66,66,66,66,66],
        [66,13,66,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [66,66,69,66,66,66,66,66,66,66,66,66,66,66,66,66,66],
        [66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,8,66],
        [66,66,66,66,66,66,66,66,6,66,66,66,66,66,66,66,66],
        [66,66,70,66,66,9,66,66,66,66,66,66,66,66,66,66,66],
        [66,66,66,66,66,66,66,66,66,66,66,7,66,66,66,66,66],
        [66,66,71,66,66,66,66,66,66,66,66,66,66,66,66,66,66],
        [66,66,72,66,66,66,66,66,66,66,66,66,66,66,66,66,66],
        [66,66,73,66,66,66,66,66,66,66,66,66,66,66,66,66,66],
        [66,13,66,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [74,66,74,74,74,74,74,74,66,66,74,66,66,66,66,66,66],
        [66,66,14,19,27,66,28,29,66,66,30,66,66,66,66,66,66],
        [66,16,66,66,66,66,62,66,66,66,66,38,61,60,66,66,66],
        [75,66,75,75,75,75,75,75,66,66,75,66,66,66,66,66,66],
        [66,66,17,49,56,66,57,58,66,66,59,66,66,66,66,66,66],
        [66,13,66,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [76,66,76,76,76,76,76,76,66,66,30,66,66,66,66,66,66],
        [77,66,77,19,77,77,77,29,66,66,30,66,66,66,66,66,66],
        [78,66,78,19,78,78,78,29,66,66,30,66,66,66,66,66,66],
        [79,66,79,79,79,79,79,79,66,66,30,66,66,66,66,66,66],
        [80,66,80,80,80,80,80,80,66,66,30,66,66,66,66,66,66],
        [81,66,81,81,81,81,81,81,66,66,81,66,66,66,66,66,66],
        [82,66,82,19,27,82,28,29,66,66,30,66,66,66,66,66,66],
        [66,13,66,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [66,13,66,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [66,13,66,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [66,13,66,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [83,66,83,83,83,83,83,83,66,66,83,66,66,66,66,66,66],
        [84,66,84,84,84,84,84,84,66,66,84,66,66,66,66,66,66],
        [66,13,66,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [85,35,85,85,85,85,85,85,66,66,85,66,66,66,66,66,66],
        [66,13,86,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [87,66,87,87,87,87,87,87,66,66,87,66,66,66,66,66,66],
        [66,66,36,66,66,66,66,66,66,66,66,66,66,66,66,66,66],
        [88,39,88,88,88,88,88,88,66,66,88,66,66,66,66,66,66],
        [66,13,86,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [89,66,89,89,89,89,89,89,66,66,89,66,66,66,66,66,66],
        [66,66,40,66,66,66,66,66,66,66,66,66,66,66,66,66,66],
        [66,16,66,66,66,66,62,66,66,66,66,38,61,60,66,66,66],
        [66,66,66,66,66,66,66,66,66,66,66,44,66,66,66,66,66],
        [66,45,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66],
        [66,66,90,66,66,66,66,66,66,66,66,7,66,66,66,66,66],
        [66,66,66,66,66,66,66,66,66,42,66,66,66,66,66,66,66],
        [66,66,46,66,66,66,66,66,66,66,66,66,66,66,66,66,66],
        [91,66,91,49,56,91,57,58,66,66,59,66,66,66,66,66,66],
        [66,16,66,66,66,66,62,66,66,66,66,38,61,60,66,66,66],
        [92,66,92,92,92,92,92,92,66,66,59,66,66,66,66,66,66],
        [93,66,93,49,93,93,93,58,66,66,59,66,66,66,66,66,66],
        [94,66,94,49,94,94,94,58,66,66,59,66,66,66,66,66,66],
        [95,66,95,95,95,95,95,95,66,66,59,66,66,66,66,66,66],
        [96,66,96,96,96,96,96,96,66,66,59,66,66,66,66,66,66],
        [97,66,97,97,97,97,97,97,66,66,97,66,66,66,66,66,66],
        [66,16,66,66,66,66,62,66,66,66,66,38,61,60,66,66,66],
        [66,16,66,66,66,66,62,66,66,66,66,38,61,60,66,66,66],
        [66,16,66,66,66,66,62,66,66,66,66,38,61,60,66,66,66],
        [66,16,66,66,66,66,62,66,66,66,66,38,61,60,66,66,66],
        [98,66,98,98,98,98,98,98,66,66,98,66,66,66,66,66,66],
        [99,66,99,99,99,99,99,99,66,66,99,66,66,66,66,66,66],
        [66,16,66,66,66,66,62,66,66,66,66,38,61,60,66,66,66],
        [66,13,66,66,66,66,33,66,66,66,66,34,32,31,65,66,43],
        [66,66,66,66,66,66,66,66,66,63,66,66,66,66,66,66,66],
        [66,66,66,66,66,66,66,66,66,66,66,64,66,66,66,66,66]
        ]
    GOTO = [
        [2,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [3,5,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,10,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [15,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,18,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [20,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [21,0,0,0,0,0],
        [22,0,0,0,0,0],
        [23,0,0,0,0,0],
        [24,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [25,0,0,0,0,0],
        [0,0,0,0,0,0],
        [3,12,0,0,37,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [3,12,0,0,41,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,48,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,11,0,0,47],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,50,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,51,0,0],
        [0,0,0,52,0,0],
        [0,0,0,53,0,0],
        [0,0,0,54,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,55,0,0],
        [26,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]
        ]
    def __init__(self, lex, debug=False):
        self.lex = lex
        self.debug = debug
        self.stack = deque()
    def top(self):
        if len(self.stack)>0:
            return self.stack[-1][0]
        else:
            return 0
    def parse(self):
        a = self.lex.getNextToken()
        while True:
            action = self.Action[self.top()][int(a[0])]
            if action == 67:
                self.stack.pop()
                return self.stack.pop()[1]
            elif action == 90:
                if self.debug: print("Reduce using Args -> ")
                
                gt = self.GOTO[self.top()][5] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 72:
                if self.debug: print("Reduce using Args -> Args1")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][5] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 70:
                if self.debug: print("Reduce using Args1 -> id doublep type")
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([makeFArgs(Param,_1, _3)])))
            elif action == 71:
                if self.debug: print("Reduce using Args1 -> id doublep type comma Args1")
                _5 = self.stack.pop()[1]
                _4 = self.stack.pop()[1][1]
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([makeFArgs(Param,_1, _3)] + _5)))
            elif action == 68:
                if self.debug: print("Reduce using Args1Call -> E")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][1] # Args1Call
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 69:
                if self.debug: print("Reduce using Args1Call -> E comma Args1Call")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][1] # Args1Call
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1] + _3)))
            elif action == 86:
                if self.debug: print("Reduce using ArgsCall -> ")
                
                gt = self.GOTO[self.top()][4] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 73:
                if self.debug: print("Reduce using ArgsCall -> Args1Call")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][4] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 83:
                if self.debug: print("Reduce using E -> float")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(Literal, _1, "float"))))
            elif action == 91:
                if self.debug: print("Reduce using E -> func id lparen Args rparen assign FBody")
                _7 = self.stack.pop()[1]
                _6 = self.stack.pop()[1][1]
                _5 = self.stack.pop()[1][1]
                _4 = self.stack.pop()[1]
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeF(_2, _4, _7))))
            elif action == 85:
                if self.debug: print("Reduce using E -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeId(Id, _1))))
            elif action == 87:
                if self.debug: print("Reduce using E -> id lparen ArgsCall rparen")
                _4 = self.stack.pop()[1][1]
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeC(Call, _1, _3))))
            elif action == 84:
                if self.debug: print("Reduce using E -> int")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(Literal, _1, "int"))))
            elif action == 82:
                if self.debug: print("Reduce using E -> let id assign E")
                _4 = self.stack.pop()[1]
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeId(Assign, _2, _4))))
            elif action == 74:
                if self.debug: print("Reduce using E -> lparen E rparen")
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_2)))
            elif action == 81:
                if self.debug: print("Reduce using E -> minus E")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(UnaryOp, '-', _2))))
            elif action == 79:
                if self.debug: print("Reduce using E -> E del E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(BinaryOp, '/', _1, _3))))
            elif action == 78:
                if self.debug: print("Reduce using E -> E minus E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(BinaryOp, '-', _1, _3))))
            elif action == 76:
                if self.debug: print("Reduce using E -> E mul E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(BinaryOp, '*', _1, _3))))
            elif action == 77:
                if self.debug: print("Reduce using E -> E plus E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(BinaryOp, '+', _1, _3))))
            elif action == 80:
                if self.debug: print("Reduce using E -> E pow E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(BinaryOp,'^', _1, _3))))
            elif action == 98:
                if self.debug: print("Reduce using FBody -> float")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(Literal, _1, "float"))))
            elif action == 88:
                if self.debug: print("Reduce using FBody -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBodyParam(Id, _1))))
            elif action == 89:
                if self.debug: print("Reduce using FBody -> id lparen ArgsCall rparen")
                _4 = self.stack.pop()[1][1]
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeC(Call, _1, _3))))
            elif action == 99:
                if self.debug: print("Reduce using FBody -> int")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(Literal, _1, "int"))))
            elif action == 75:
                if self.debug: print("Reduce using FBody -> lparen FBody rparen")
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_2)))
            elif action == 97:
                if self.debug: print("Reduce using FBody -> minus FBody")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(UnaryOp, '-', _2))))
            elif action == 95:
                if self.debug: print("Reduce using FBody -> FBody del FBody")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(BinaryOp, '/', _1, _3))))
            elif action == 94:
                if self.debug: print("Reduce using FBody -> FBody minus FBody")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(BinaryOp, '-', _1, _3))))
            elif action == 92:
                if self.debug: print("Reduce using FBody -> FBody mul FBody")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(BinaryOp, '*', _1, _3))))
            elif action == 93:
                if self.debug: print("Reduce using FBody -> FBody plus FBody")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(BinaryOp, '+', _1, _3))))
            elif action == 96:
                if self.debug: print("Reduce using FBody -> FBody pow FBody")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(BinaryOp,'^', _1, _3))))
            elif action == 66:
                lastSt = self.top()
                parsed=stateToString(lastSt)
                while len(self.stack) > 0:
                    self.stack.pop()
                    parsed = stateToString(self.top()) + " " + parsed
                raise Exception(
                  f'Rejection state reached after parsing "{parsed}", when encoutered symbol "{a[0].name}" in state {lastSt}. Expected "{expectedSym(lastSt)}"')
            else:
                if self.debug: print(f"Shift to {action}")
                self.stack.append((action, a))
                a=self.lex.getNextToken()