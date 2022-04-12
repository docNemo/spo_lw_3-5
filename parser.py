from lexer import *
from enum import IntEnum
from collections import deque


from classes import *


def stateToString(state):
  return [ ".","%eof","E","doublep","id","type","comma","Args1","E","comma","Args1Call","Args1","Args1Call","lparen","rparen","E","mul","E","E","E","E","E","E","E","E","plus","minus","del","pow","id","lparen","rparen","ArgsCall","float","int","minus","assign","func","id","lparen","rparen","Args","assign","id","let" ][state]

def expectedSym(state):
  return [ "E","%eof","%eof/mul/plus/minus/del/pow","type/type","doublep/doublep","rparen/comma","Args1","rparen","rparen/comma/mul/plus/minus/del/pow","Args1Call","rparen","rparen","rparen","E","%eof/comma/del/minus/mul/plus/pow/rparen","rparen/mul/plus/minus/del/pow","E","mul/%eof/comma/del/minus/mul/plus/pow/rparen/plus/minus/del/pow","mul/plus/%eof/comma/del/minus/mul/plus/pow/rparen/minus/del/pow","mul/plus/minus/%eof/comma/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/del/%eof/comma/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","E","E","E","E","lparen/%eof/comma/del/minus/mul/plus/pow/rparen","ArgsCall","%eof/comma/del/minus/mul/plus/pow/rparen","rparen","%eof/comma/del/minus/mul/plus/pow/rparen","%eof/comma/del/minus/mul/plus/pow/rparen","E","E","id","lparen","Args","assign","rparen","E","assign","id" ][state]

class Parser:
    Action = [
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [46,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [1,45,45,16,25,45,26,27,45,45,28,45,45,45,45,45,45],
        [45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,5,45],
        [45,45,45,45,45,45,45,45,3,45,45,45,45,45,45,45,45],
        [45,45,47,45,45,6,45,45,45,45,45,45,45,45,45,45,45],
        [45,45,45,45,45,45,45,45,45,45,45,4,45,45,45,45,45],
        [45,45,48,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,45,49,16,25,9,26,27,45,45,28,45,45,45,45,45,45],
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [45,45,50,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,45,51,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,45,52,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [53,45,53,53,53,53,53,53,45,45,53,45,45,45,45,45,45],
        [45,45,14,16,25,45,26,27,45,45,28,45,45,45,45,45,45],
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [54,45,54,54,54,54,54,54,45,45,28,45,45,45,45,45,45],
        [55,45,55,16,55,55,55,27,45,45,28,45,45,45,45,45,45],
        [56,45,56,16,56,56,56,27,45,45,28,45,45,45,45,45,45],
        [57,45,57,57,57,57,57,57,45,45,28,45,45,45,45,45,45],
        [58,45,58,58,58,58,58,58,45,45,28,45,45,45,45,45,45],
        [59,45,59,59,59,59,59,59,45,45,59,45,45,45,45,45,45],
        [60,45,60,16,25,60,26,27,45,45,28,45,45,45,45,45,45],
        [61,45,61,16,25,61,26,27,45,45,28,45,45,45,45,45,45],
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [62,30,62,62,62,62,62,62,45,45,62,45,45,45,45,45,45],
        [45,13,63,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [64,45,64,64,64,64,64,64,45,45,64,45,45,45,45,45,45],
        [45,45,31,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [65,45,65,65,65,65,65,65,45,45,65,45,45,45,45,45,45],
        [66,45,66,66,66,66,66,66,45,45,66,45,45,45,45,45,45],
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [45,45,45,45,45,45,45,45,45,45,45,38,45,45,45,45,45],
        [45,39,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,45,67,45,45,45,45,45,45,45,45,4,45,45,45,45,45],
        [45,45,45,45,45,45,45,45,45,36,45,45,45,45,45,45,45],
        [45,45,40,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,13,45,45,45,45,35,45,45,45,45,29,34,33,44,45,37],
        [45,45,45,45,45,45,45,45,45,42,45,45,45,45,45,45,45],
        [45,45,45,45,45,45,45,45,45,45,45,43,45,45,45,45,45]
        ]
    GOTO = [
        [2,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,7,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [8,0,10,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [15,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [17,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [18,0,0,0,0],
        [19,0,0,0,0],
        [20,0,0,0,0],
        [21,0,0,0,0],
        [0,0,0,0,0],
        [8,0,12,32,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [22,0,0,0,0],
        [23,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,11,0,0,41],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [24,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0]
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
            if action == 46:
                self.stack.pop()
                return self.stack.pop()[1]
            elif action == 67:
                if self.debug: print("Reduce using Args -> ")
                
                gt = self.GOTO[self.top()][4] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 51:
                if self.debug: print("Reduce using Args -> Args1")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][4] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 47:
                if self.debug: print("Reduce using Args1 -> id doublep type")
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][1] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([Param,_1, _3])))
            elif action == 48:
                if self.debug: print("Reduce using Args1 -> id doublep type comma Args1")
                _5 = self.stack.pop()[1]
                _4 = self.stack.pop()[1][1]
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][1] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([Param,_1, _3] + _5)))
            elif action == 49:
                if self.debug: print("Reduce using Args1Call -> E")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][2] # Args1Call
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 50:
                if self.debug: print("Reduce using Args1Call -> E comma Args1Call")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][2] # Args1Call
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1] + _3)))
            elif action == 63:
                if self.debug: print("Reduce using ArgsCall -> ")
                
                gt = self.GOTO[self.top()][3] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 52:
                if self.debug: print("Reduce using ArgsCall -> Args1Call")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][3] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 65:
                if self.debug: print("Reduce using E -> float")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(Literal, _1, "float"))))
            elif action == 60:
                if self.debug: print("Reduce using E -> func id lparen Args rparen assign E")
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
            elif action == 62:
                if self.debug: print("Reduce using E -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(makeId(Id, _1))))
            elif action == 64:
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
                self.stack.append((gt,(make(Call, _1, _3))))
            elif action == 66:
                if self.debug: print("Reduce using E -> int")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(Literal, _1, "int"))))
            elif action == 61:
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
            elif action == 53:
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
            elif action == 59:
                if self.debug: print("Reduce using E -> minus E")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(make(UnaryOp, '-', _2))))
            elif action == 57:
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
            elif action == 56:
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
            elif action == 54:
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
            elif action == 55:
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
            elif action == 58:
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
            elif action == 45:
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