from lexer import *
from enum import IntEnum
from collections import deque


from classes import *


def stateToString(state):
  return [ ".","%eof","E","E","FBody","comma","Args1Call","comma","Args1CallF","doublep","id","type","comma","Args1","Args1","Args1Call","Args1CallF","lparen","rparen","E","lparen","rparen","FBody","mul","E","E","E","E","E","E","E","plus","minus","del","pow","float","int","minus","id","lparen","rparen","ArgsCall","id","lparen","rparen","ArgsCallF","assign","func","id","lparen","rparen","Args","FBody","mul","FBody","FBody","FBody","FBody","FBody","FBody","plus","minus","del","pow","float","int","minus","assign","id","let" ][state]

def expectedSym(state):
  return [ "E","%eof","%eof/mul/plus/minus/del/pow","rparen/comma/mul/plus/minus/del/pow","rparen/comma/mul/plus/minus/del/pow","Args1Call","rparen","Args1CallF","rparen","type/type","doublep/doublep","rparen/comma","Args1","rparen","rparen","rparen","rparen","E","%eof/comma/del/minus/mul/plus/pow/rparen","rparen/mul/plus/minus/del/pow","FBody","%eof/comma/del/minus/mul/plus/pow/rparen","rparen/mul/plus/minus/del/pow","E","mul/%eof/comma/del/minus/mul/plus/pow/rparen/plus/minus/del/pow","mul/plus/%eof/comma/del/minus/mul/plus/pow/rparen/minus/del/pow","mul/plus/minus/%eof/comma/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/del/%eof/comma/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","E","E","E","E","%eof/comma/del/minus/mul/plus/pow/rparen","%eof/comma/del/minus/mul/plus/pow/rparen","E","lparen/%eof/comma/del/minus/mul/plus/pow/rparen","ArgsCall","%eof/comma/del/minus/mul/plus/pow/rparen","rparen","lparen/%eof/comma/del/minus/mul/plus/pow/rparen","ArgsCallF","%eof/comma/del/minus/mul/plus/pow/rparen","rparen","FBody","id","lparen","Args","assign","rparen","%eof/comma/del/minus/mul/plus/pow/rparen/mul/plus/minus/del/pow","FBody","mul/%eof/comma/del/minus/mul/plus/pow/rparen/plus/minus/del/pow","mul/plus/%eof/comma/del/minus/mul/plus/pow/rparen/minus/del/pow","mul/plus/minus/%eof/comma/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/del/%eof/comma/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","FBody","FBody","FBody","FBody","%eof/comma/del/minus/mul/plus/pow/rparen","%eof/comma/del/minus/mul/plus/pow/rparen","FBody","E","assign","id" ][state]

class Parser:
    Action = [
        [70,17,70,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [71,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [1,70,70,23,31,70,32,33,70,70,34,70,70,70,70,70,70],
        [70,70,72,23,31,5,32,33,70,70,34,70,70,70,70,70,70],
        [70,70,73,53,60,7,61,62,70,70,63,70,70,70,70,70,70],
        [70,17,70,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [70,70,74,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [70,20,70,70,70,70,66,70,70,70,70,42,65,64,70,70,70],
        [70,70,75,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,11,70],
        [70,70,70,70,70,70,70,70,9,70,70,70,70,70,70,70,70],
        [70,70,76,70,70,12,70,70,70,70,70,70,70,70,70,70,70],
        [70,70,70,70,70,70,70,70,70,70,70,10,70,70,70,70,70],
        [70,70,77,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [70,70,78,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [70,70,79,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [70,70,80,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [70,17,70,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [81,70,81,81,81,81,81,81,70,70,81,70,70,70,70,70,70],
        [70,70,18,23,31,70,32,33,70,70,34,70,70,70,70,70,70],
        [70,20,70,70,70,70,66,70,70,70,70,42,65,64,70,70,70],
        [82,70,82,82,82,82,82,82,70,70,82,70,70,70,70,70,70],
        [70,70,21,53,60,70,61,62,70,70,63,70,70,70,70,70,70],
        [70,17,70,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [83,70,83,83,83,83,83,83,70,70,34,70,70,70,70,70,70],
        [84,70,84,23,84,84,84,33,70,70,34,70,70,70,70,70,70],
        [85,70,85,23,85,85,85,33,70,70,34,70,70,70,70,70,70],
        [86,70,86,86,86,86,86,86,70,70,34,70,70,70,70,70,70],
        [87,70,87,87,87,87,87,87,70,70,34,70,70,70,70,70,70],
        [88,70,88,88,88,88,88,88,70,70,88,70,70,70,70,70,70],
        [89,70,89,23,31,89,32,33,70,70,34,70,70,70,70,70,70],
        [70,17,70,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [70,17,70,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [70,17,70,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [70,17,70,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [90,70,90,90,90,90,90,90,70,70,90,70,70,70,70,70,70],
        [91,70,91,91,91,91,91,91,70,70,91,70,70,70,70,70,70],
        [70,17,70,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [92,39,92,92,92,92,92,92,70,70,92,70,70,70,70,70,70],
        [70,17,93,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [94,70,94,94,94,94,94,94,70,70,94,70,70,70,70,70,70],
        [70,70,40,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [95,43,95,95,95,95,95,95,70,70,95,70,70,70,70,70,70],
        [70,20,96,70,70,70,66,70,70,70,70,42,65,64,70,70,70],
        [97,70,97,97,97,97,97,97,70,70,97,70,70,70,70,70,70],
        [70,70,44,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [70,20,70,70,70,70,66,70,70,70,70,42,65,64,70,70,70],
        [70,70,70,70,70,70,70,70,70,70,70,48,70,70,70,70,70],
        [70,49,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [70,70,98,70,70,70,70,70,70,70,70,10,70,70,70,70,70],
        [70,70,70,70,70,70,70,70,70,46,70,70,70,70,70,70,70],
        [70,70,50,70,70,70,70,70,70,70,70,70,70,70,70,70,70],
        [99,70,99,53,60,99,61,62,70,70,63,70,70,70,70,70,70],
        [70,20,70,70,70,70,66,70,70,70,70,42,65,64,70,70,70],
        [100,70,100,100,100,100,100,100,70,70,63,70,70,70,70,70,70],
        [101,70,101,53,101,101,101,62,70,70,63,70,70,70,70,70,70],
        [102,70,102,53,102,102,102,62,70,70,63,70,70,70,70,70,70],
        [103,70,103,103,103,103,103,103,70,70,63,70,70,70,70,70,70],
        [104,70,104,104,104,104,104,104,70,70,63,70,70,70,70,70,70],
        [105,70,105,105,105,105,105,105,70,70,105,70,70,70,70,70,70],
        [70,20,70,70,70,70,66,70,70,70,70,42,65,64,70,70,70],
        [70,20,70,70,70,70,66,70,70,70,70,42,65,64,70,70,70],
        [70,20,70,70,70,70,66,70,70,70,70,42,65,64,70,70,70],
        [70,20,70,70,70,70,66,70,70,70,70,42,65,64,70,70,70],
        [106,70,106,106,106,106,106,106,70,70,106,70,70,70,70,70,70],
        [107,70,107,107,107,107,107,107,70,70,107,70,70,70,70,70,70],
        [70,20,70,70,70,70,66,70,70,70,70,42,65,64,70,70,70],
        [70,17,70,70,70,70,37,70,70,70,70,38,36,35,69,70,47],
        [70,70,70,70,70,70,70,70,70,67,70,70,70,70,70,70,70],
        [70,70,70,70,70,70,70,70,70,70,70,68,70,70,70,70,70]
        ]
    GOTO = [
        [2,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [3,6,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,8,4,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,13,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [19,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,22,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [24,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [25,0,0,0,0,0,0,0],
        [26,0,0,0,0,0,0,0],
        [27,0,0,0,0,0,0,0],
        [28,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [29,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [3,15,0,0,0,41,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,16,4,0,0,45,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,52,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,14,0,0,51],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,54,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,55,0,0,0,0],
        [0,0,0,56,0,0,0,0],
        [0,0,0,57,0,0,0,0],
        [0,0,0,58,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,59,0,0,0,0],
        [30,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
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
            if action == 71:
                self.stack.pop()
                return self.stack.pop()[1]
            elif action == 98:
                if self.debug: print("Reduce using Args -> ")
                
                gt = self.GOTO[self.top()][7] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 78:
                if self.debug: print("Reduce using Args -> Args1")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][7] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 76:
                if self.debug: print("Reduce using Args1 -> id doublep type")
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][4] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([makeFArgs(Param,_1, _3)])))
            elif action == 77:
                if self.debug: print("Reduce using Args1 -> id doublep type comma Args1")
                _5 = self.stack.pop()[1]
                _4 = self.stack.pop()[1][1]
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][4] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([makeFArgs(Param,_1, _3)] + _5)))
            elif action == 72:
                if self.debug: print("Reduce using Args1Call -> E")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][1] # Args1Call
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 74:
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
            elif action == 73:
                if self.debug: print("Reduce using Args1CallF -> FBody")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][2] # Args1CallF
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 75:
                if self.debug: print("Reduce using Args1CallF -> FBody comma Args1CallF")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][2] # Args1CallF
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1] + _3)))
            elif action == 93:
                if self.debug: print("Reduce using ArgsCall -> ")
                
                gt = self.GOTO[self.top()][5] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 79:
                if self.debug: print("Reduce using ArgsCall -> Args1Call")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][5] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 96:
                if self.debug: print("Reduce using ArgsCallF -> ")
                
                gt = self.GOTO[self.top()][6] # ArgsCallF
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 80:
                if self.debug: print("Reduce using ArgsCallF -> Args1CallF")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][6] # ArgsCallF
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 90:
                if self.debug: print("Reduce using E -> float")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(Literal, _1, "float"))))
            elif action == 99:
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
            elif action == 92:
                if self.debug: print("Reduce using E -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeId(Id, _1))))
            elif action == 94:
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
            elif action == 91:
                if self.debug: print("Reduce using E -> int")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(Literal, _1, "int"))))
            elif action == 89:
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
            elif action == 81:
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
            elif action == 88:
                if self.debug: print("Reduce using E -> minus E")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(UnaryOp, '-', _2))))
            elif action == 86:
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
            elif action == 85:
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
            elif action == 83:
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
            elif action == 84:
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
            elif action == 87:
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
            elif action == 106:
                if self.debug: print("Reduce using FBody -> float")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(Literal, _1, "float"))))
            elif action == 95:
                if self.debug: print("Reduce using FBody -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBodyParam(Id, _1))))
            elif action == 97:
                if self.debug: print("Reduce using FBody -> id lparen ArgsCallF rparen")
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
            elif action == 107:
                if self.debug: print("Reduce using FBody -> int")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(Literal, _1, "int"))))
            elif action == 82:
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
            elif action == 105:
                if self.debug: print("Reduce using FBody -> minus FBody")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][3] # FBody
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeFBody(UnaryOp, '-', _2))))
            elif action == 103:
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
            elif action == 102:
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
            elif action == 100:
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
            elif action == 101:
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
            elif action == 104:
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
            elif action == 70:
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