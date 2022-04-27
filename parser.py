from lexer import *
from enum import IntEnum
from collections import deque


from classes import *


def stateToString(state):
  return [ ".","%eof","SS","id","doublep","id","type","comma","Args1","E","S","comma","Args1Call","semicol","SS","Args1","Args1Call","lparen","rparen","E","mul","E","E","E","E","E","E","E","E","E","plus","minus","del","pow","float","int","minus","lparen","rparen","ArgsCall","assign","func","id","lparen","rparen","Args","assign","id","let","A","D" ][state]

def expectedSym(state):
  return [ "SS","%eof","%eof","%eof/comma/del/minus/mul/plus/pow/rparen/semicol/lparen","type/type","doublep/doublep","rparen/comma","Args1","rparen","rparen/comma/mul/plus/minus/del/pow","%eof/semicol","Args1Call","rparen","SS","%eof","rparen","rparen","E","%eof/comma/del/minus/mul/plus/pow/rparen/semicol","rparen/mul/plus/minus/del/pow","E","mul/%eof/comma/del/minus/mul/plus/pow/rparen/semicol/plus/minus/del/pow","mul/plus/%eof/comma/del/minus/mul/plus/pow/rparen/semicol/minus/del/pow","mul/plus/minus/%eof/comma/del/minus/mul/plus/pow/rparen/semicol/del/pow","mul/plus/minus/del/%eof/comma/del/minus/mul/plus/pow/rparen/semicol/pow","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen/semicol","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen/semicol","mul/plus/minus/del/pow/%eof/semicol","mul/plus/minus/del/pow/%eof/semicol","mul/plus/minus/del/pow/%eof/semicol","E","E","E","E","%eof/comma/del/minus/mul/plus/pow/rparen/semicol","%eof/comma/del/minus/mul/plus/pow/rparen/semicol","E","ArgsCall","%eof/comma/del/minus/mul/plus/pow/rparen/semicol","rparen","E","id","lparen","Args","assign","rparen","E","assign","id","%eof/semicol","%eof/semicol" ][state]

class Parser:
    Action = [
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,48,51,41],
        [52,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],
        [1,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],
        [53,37,53,53,53,53,53,53,51,53,51,53,51,51,51,51,51,51],
        [51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,6,51],
        [51,51,51,51,51,51,51,51,4,51,51,51,51,51,51,51,51,51],
        [51,51,54,51,51,7,51,51,51,51,51,51,51,51,51,51,51,51],
        [51,51,51,51,51,51,51,51,51,51,51,51,5,51,51,51,51,51],
        [51,51,55,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],
        [51,51,56,20,30,11,31,32,51,51,51,33,51,51,51,51,51,51],
        [57,51,51,51,51,51,51,51,51,13,51,51,51,51,51,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [51,51,58,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,48,51,41],
        [59,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],
        [51,51,60,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],
        [51,51,61,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [62,51,62,62,62,62,62,62,51,62,51,62,51,51,51,51,51,51],
        [51,51,18,20,30,51,31,32,51,51,51,33,51,51,51,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [63,51,63,63,63,63,63,63,51,63,51,33,51,51,51,51,51,51],
        [64,51,64,20,64,64,64,32,51,64,51,33,51,51,51,51,51,51],
        [65,51,65,20,65,65,65,32,51,65,51,33,51,51,51,51,51,51],
        [66,51,66,66,66,66,66,66,51,66,51,33,51,51,51,51,51,51],
        [67,51,67,67,67,67,67,67,51,67,51,33,51,51,51,51,51,51],
        [68,51,68,68,68,68,68,68,51,68,51,68,51,51,51,51,51,51],
        [69,51,51,20,30,51,31,32,51,69,51,33,51,51,51,51,51,51],
        [70,51,51,20,30,51,31,32,51,70,51,33,51,51,51,51,51,51],
        [71,51,51,20,30,51,31,32,51,71,51,33,51,51,51,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [72,51,72,72,72,72,72,72,51,72,51,72,51,51,51,51,51,51],
        [73,51,73,73,73,73,73,73,51,73,51,73,51,51,51,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [51,17,74,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [75,51,75,75,75,75,75,75,51,75,51,75,51,51,51,51,51,51],
        [51,51,38,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [51,51,51,51,51,51,51,51,51,51,51,51,42,51,51,51,51,51],
        [51,43,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],
        [51,51,76,51,51,51,51,51,51,51,51,51,5,51,51,51,51,51],
        [51,51,51,51,51,51,51,51,51,51,40,51,51,51,51,51,51,51],
        [51,51,44,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],
        [51,17,51,51,51,51,36,51,51,51,51,51,3,35,34,51,51,51],
        [51,51,51,51,51,51,51,51,51,51,46,51,51,51,51,51,51,51],
        [51,51,51,51,51,51,51,51,51,51,51,51,47,51,51,51,51,51],
        [77,51,51,51,51,51,51,51,51,77,51,51,51,51,51,51,51,51],
        [78,51,51,51,51,51,51,51,51,78,51,51,51,51,51,51,51,51]
        ]
    GOTO = [
        [49,50,29,10,2,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,8,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,9,0,0,0,12,0,0],
        [0,0,0,0,0,0,0,0,0],
        [49,50,29,10,14,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,19,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,21,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,22,0,0,0,0,0,0],
        [0,0,23,0,0,0,0,0,0],
        [0,0,24,0,0,0,0,0,0],
        [0,0,25,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,26,0,0,0,0,0,0],
        [0,0,9,0,0,0,16,39,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,27,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,15,0,0,45],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,28,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
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
            if action == 52:
                self.stack.pop()
                return self.stack.pop()[1]
            elif action == 70:
                if self.debug: print("Reduce using A -> let id assign E")
                _4 = self.stack.pop()[1]
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # A
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeId(Assign, _2, _4))))
            elif action == 76:
                if self.debug: print("Reduce using Args -> ")
                
                gt = self.GOTO[self.top()][8] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 60:
                if self.debug: print("Reduce using Args -> Args1")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][8] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 54:
                if self.debug: print("Reduce using Args1 -> id doublep type")
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][5] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([Param(_1, _3)])))
            elif action == 55:
                if self.debug: print("Reduce using Args1 -> id doublep type comma Args1")
                _5 = self.stack.pop()[1]
                _4 = self.stack.pop()[1][1]
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][5] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([Param(_1, _3)] + _5)))
            elif action == 56:
                if self.debug: print("Reduce using Args1Call -> E")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][6] # Args1Call
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 58:
                if self.debug: print("Reduce using Args1Call -> E comma Args1Call")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][6] # Args1Call
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1] + _3)))
            elif action == 74:
                if self.debug: print("Reduce using ArgsCall -> ")
                
                gt = self.GOTO[self.top()][7] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 61:
                if self.debug: print("Reduce using ArgsCall -> Args1Call")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][7] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 69:
                if self.debug: print("Reduce using D -> func id lparen Args rparen assign E")
                _7 = self.stack.pop()[1]
                _6 = self.stack.pop()[1][1]
                _5 = self.stack.pop()[1][1]
                _4 = self.stack.pop()[1]
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][1] # D
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeF(_2, _4, _7))))
            elif action == 72:
                if self.debug: print("Reduce using E -> float")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(Float, _1))))
            elif action == 53:
                if self.debug: print("Reduce using E -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(Id(_1))))
            elif action == 75:
                if self.debug: print("Reduce using E -> id lparen ArgsCall rparen")
                _4 = self.stack.pop()[1][1]
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeC(Call, _1, _3))))
            elif action == 73:
                if self.debug: print("Reduce using E -> int")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(Int, _1))))
            elif action == 62:
                if self.debug: print("Reduce using E -> lparen E rparen")
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_2)))
            elif action == 68:
                if self.debug: print("Reduce using E -> minus E")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(UnaryOp, '-', _2))))
            elif action == 66:
                if self.debug: print("Reduce using E -> E del E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(BinaryOp, '/', _1, _3))))
            elif action == 65:
                if self.debug: print("Reduce using E -> E minus E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(BinaryOp, '-', _1, _3))))
            elif action == 63:
                if self.debug: print("Reduce using E -> E mul E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(BinaryOp, '*', _1, _3))))
            elif action == 64:
                if self.debug: print("Reduce using E -> E plus E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(BinaryOp, '+', _1, _3))))
            elif action == 67:
                if self.debug: print("Reduce using E -> E pow E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(BinaryOp,'^', _1, _3))))
            elif action == 77:
                if self.debug: print("Reduce using S -> A")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][3] # S
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 78:
                if self.debug: print("Reduce using S -> D")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][3] # S
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 71:
                if self.debug: print("Reduce using S -> E")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][3] # S
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 57:
                if self.debug: print("Reduce using SS -> S")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][4] # SS
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 59:
                if self.debug: print("Reduce using SS -> S semicol SS")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][4] # SS
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1] + _3)))
            elif action == 51:
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