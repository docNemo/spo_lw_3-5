from lexer import *
from enum import IntEnum
from collections import deque


import classes


def stateToString(state):
  return [ ".","%eof","E","assign","func","id","lparen","rparen","Args","E","E","comma","Args1Call","doublep","id","type","comma","Args1","Args1","Args1Call","lparen","rparen","E","assign","id","let","E","mul","E","E","E","E","E","E","plus","minus","del","pow","id","lparen","rparen","ArgsCall","float","int","minus" ][state]

def expectedSym(state):
  return [ "E","%eof","%eof/mul/plus/minus/del/pow","E","id","lparen","Args","assign","rparen","%eof/comma/del/minus/mul/plus/pow/rparen/mul/plus/minus/del/pow","rparen/comma/mul/plus/minus/del/pow","Args1Call","rparen","type/type","doublep/doublep","rparen/comma","Args1","rparen","rparen","rparen","E","%eof/comma/del/minus/mul/plus/pow/rparen","rparen/mul/plus/minus/del/pow","E","assign","id","%eof/comma/del/minus/mul/plus/pow/rparen/mul/plus/minus/del/pow","E","mul/%eof/comma/del/minus/mul/plus/pow/rparen/plus/minus/del/pow","mul/plus/%eof/comma/del/minus/mul/plus/pow/rparen/minus/del/pow","mul/plus/minus/%eof/comma/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/del/%eof/comma/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen","E","E","E","E","lparen/%eof/comma/del/minus/mul/plus/pow/rparen","ArgsCall","%eof/comma/del/minus/mul/plus/pow/rparen","rparen","%eof/comma/del/minus/mul/plus/pow/rparen","%eof/comma/del/minus/mul/plus/pow/rparen","E" ][state]

class Parser:
    Action = [
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [46,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [1,45,45,27,34,45,35,36,45,45,37,45,45,45,45,45,45],
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [45,45,45,45,45,45,45,45,45,45,45,5,45,45,45,45,45],
        [45,6,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,45,47,45,45,45,45,45,45,45,45,14,45,45,45,45,45],
        [45,45,45,45,45,45,45,45,45,3,45,45,45,45,45,45,45],
        [45,45,7,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [48,45,48,27,34,48,35,36,45,45,37,45,45,45,45,45,45],
        [45,45,49,27,34,11,35,36,45,45,37,45,45,45,45,45,45],
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [45,45,50,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,15,45],
        [45,45,45,45,45,45,45,45,13,45,45,45,45,45,45,45,45],
        [45,45,51,45,45,16,45,45,45,45,45,45,45,45,45,45,45],
        [45,45,45,45,45,45,45,45,45,45,45,14,45,45,45,45,45],
        [45,45,52,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,45,53,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,45,54,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [55,45,55,55,55,55,55,55,45,45,55,45,45,45,45,45,45],
        [45,45,21,27,34,45,35,36,45,45,37,45,45,45,45,45,45],
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [45,45,45,45,45,45,45,45,45,23,45,45,45,45,45,45,45],
        [45,45,45,45,45,45,45,45,45,45,45,24,45,45,45,45,45],
        [56,45,56,27,34,56,35,36,45,45,37,45,45,45,45,45,45],
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [57,45,57,57,57,57,57,57,45,45,37,45,45,45,45,45,45],
        [58,45,58,27,58,58,58,36,45,45,37,45,45,45,45,45,45],
        [59,45,59,27,59,59,59,36,45,45,37,45,45,45,45,45,45],
        [60,45,60,60,60,60,60,60,45,45,37,45,45,45,45,45,45],
        [61,45,61,61,61,61,61,61,45,45,37,45,45,45,45,45,45],
        [62,45,62,62,62,62,62,62,45,45,62,45,45,45,45,45,45],
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [63,39,63,63,63,63,63,63,45,45,63,45,45,45,45,45,45],
        [45,20,64,45,45,45,44,45,45,45,45,38,43,42,25,45,4],
        [65,45,65,65,65,65,65,65,45,45,65,45,45,45,45,45,45],
        [45,45,40,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
        [66,45,66,66,66,66,66,66,45,45,66,45,45,45,45,45,45],
        [67,45,67,67,67,67,67,67,45,45,67,45,45,45,45,45,45],
        [45,20,45,45,45,45,44,45,45,45,45,38,43,42,25,45,4]
        ]
    GOTO = [
        [2,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [9,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,8,18,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [10,0,0,12,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,17,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [22,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [26,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [28,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [29,0,0,0,0],
        [30,0,0,0,0],
        [31,0,0,0,0],
        [32,0,0,0,0],
        [0,0,0,0,0],
        [10,0,0,19,41],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [33,0,0,0,0]
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
            elif action == 47:
                if self.debug: print("Reduce using Args -> ")
                
                gt = self.GOTO[self.top()][1] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 53:
                if self.debug: print("Reduce using Args -> Args1")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][1] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 51:
                if self.debug: print("Reduce using Args1 -> id doublep type")
                _3 = self.stack.pop()[1][1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([classes.make(classes.Param,_1, _3)])))
            elif action == 52:
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
                self.stack.append((gt,([classes.make(classes.Param,_1, _3)] + _5)))
            elif action == 49:
                if self.debug: print("Reduce using Args1Call -> E")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][3] # Args1Call
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
                gt = self.GOTO[self.top()][3] # Args1Call
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1] + _3)))
            elif action == 64:
                if self.debug: print("Reduce using ArgsCall -> ")
                
                gt = self.GOTO[self.top()][4] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 54:
                if self.debug: print("Reduce using ArgsCall -> Args1Call")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][4] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 66:
                if self.debug: print("Reduce using E -> float")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(classes.make(classes.Literal, _1, "float"))))
            elif action == 48:
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
                self.stack.append((gt,((_2, _4, _7))))
            elif action == 63:
                if self.debug: print("Reduce using E -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(classes.make(classes.Id, _1))))
            elif action == 65:
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
                self.stack.append((gt,(classes.make(classes.Call, _1, _3))))
            elif action == 67:
                if self.debug: print("Reduce using E -> int")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(classes.make(classes.Literal, _1, "int"))))
            elif action == 56:
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
                self.stack.append((gt,(classes.make(classes.Assign, _2, _4))))
            elif action == 55:
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
            elif action == 62:
                if self.debug: print("Reduce using E -> minus E")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(classes.make(classes.UnaryOP, '-', _2))))
            elif action == 60:
                if self.debug: print("Reduce using E -> E del E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(classes.make(classes.BinaryOp, '/', _1, _3))))
            elif action == 59:
                if self.debug: print("Reduce using E -> E minus E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(classes.make(classes.BinaryOp, '-', _1, _3))))
            elif action == 57:
                if self.debug: print("Reduce using E -> E mul E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(classes.make(classes.BinaryOp, '*', _1, _3))))
            elif action == 58:
                if self.debug: print("Reduce using E -> E plus E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(classes.make(classes.BinaryOp, '+', _1, _3))))
            elif action == 61:
                if self.debug: print("Reduce using E -> E pow E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(classes.make(classes.BinaryOp,'^', _1, _3))))
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