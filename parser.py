from lexer import *
from enum import IntEnum
from collections import deque



def stateToString(state):
  return [ ".","%eof","E","mul","E","E","E","E","E","E","E","E","E","plus","minus","minus","del","assign","id","let","pow","assign","func","id","lparen","rparen","Args","id","comma","Args1","Args1","id","number","lparen","rparen" ][state]

def expectedSym(state):
  return [ "E","%eof","%eof/mul/plus/minus/del/pow","E","mul/%eof/del/minus/mul/plus/pow/rparen/plus/minus/del/pow","mul/plus/%eof/del/minus/mul/plus/pow/rparen/minus/del/pow","mul/plus/minus/%eof/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/%eof/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/del/%eof/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/%eof/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/pow/%eof/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/rparen","E","E","E","E","E","assign","id","E","E","id","lparen","Args","assign","rparen","rparen/comma","Args1","rparen","rparen","%eof/del/minus/mul/plus/pow/rparen","%eof/del/minus/mul/plus/pow/rparen","E","%eof/del/minus/mul/plus/pow/rparen" ][state]

class Parser:
    Action = [
        [35,33,35,35,35,35,15,35,35,35,31,32,19,22],
        [36,35,35,35,35,35,35,35,35,35,35,35,35,35],
        [1,35,35,3,13,35,14,16,35,20,35,35,35,35],
        [35,33,35,35,35,35,15,35,35,35,31,32,19,22],
        [37,35,37,37,37,35,37,37,35,20,35,35,35,35],
        [38,35,38,3,38,35,38,16,35,20,35,35,35,35],
        [39,35,39,3,39,35,39,16,35,20,35,35,35,35],
        [40,35,40,40,40,35,40,40,35,40,35,35,35,35],
        [41,35,41,41,41,35,41,41,35,20,35,35,35,35],
        [42,35,42,3,13,35,14,16,35,20,35,35,35,35],
        [43,35,43,43,43,35,43,43,35,20,35,35,35,35],
        [44,35,44,3,13,35,14,16,35,20,35,35,35,35],
        [35,35,34,3,13,35,14,16,35,20,35,35,35,35],
        [35,33,35,35,35,35,15,35,35,35,31,32,19,22],
        [35,33,35,35,35,35,15,35,35,35,31,32,19,22],
        [35,33,35,35,35,35,15,35,35,35,31,32,19,22],
        [35,33,35,35,35,35,15,35,35,35,31,32,19,22],
        [35,33,35,35,35,35,15,35,35,35,31,32,19,22],
        [35,35,35,35,35,35,35,35,17,35,35,35,35,35],
        [35,35,35,35,35,35,35,35,35,35,18,35,35,35],
        [35,33,35,35,35,35,15,35,35,35,31,32,19,22],
        [35,33,35,35,35,35,15,35,35,35,31,32,19,22],
        [35,35,35,35,35,35,35,35,35,35,23,35,35,35],
        [35,24,35,35,35,35,35,35,35,35,35,35,35,35],
        [35,35,45,35,35,35,35,35,35,35,27,35,35,35],
        [35,35,35,35,35,35,35,35,21,35,35,35,35,35],
        [35,35,25,35,35,35,35,35,35,35,35,35,35,35],
        [35,35,46,35,35,28,35,35,35,35,35,35,35,35],
        [35,35,35,35,35,35,35,35,35,35,27,35,35,35],
        [35,35,47,35,35,35,35,35,35,35,35,35,35,35],
        [35,35,48,35,35,35,35,35,35,35,35,35,35,35],
        [49,35,49,49,49,35,49,49,35,49,35,35,35,35],
        [50,35,50,50,50,35,50,50,35,50,35,35,35,35],
        [35,33,35,35,35,35,15,35,35,35,31,32,19,22],
        [51,35,51,51,51,35,51,51,35,51,35,35,35,35]
        ]
    GOTO = [
        [2,0,0],
        [0,0,0],
        [0,0,0],
        [4,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [5,0,0],
        [6,0,0],
        [7,0,0],
        [8,0,0],
        [9,0,0],
        [0,0,0],
        [0,0,0],
        [10,0,0],
        [11,0,0],
        [0,0,0],
        [0,0,0],
        [0,26,30],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,29],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [12,0,0],
        [0,0,0]
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
            if action == 36:
                self.stack.pop()
                return self.stack.pop()[1]
            elif action == 45:
                if self.debug: print("Reduce using Args -> ")
                
                gt = self.GOTO[self.top()][1] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 48:
                if self.debug: print("Reduce using Args -> Args1")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][1] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 46:
                if self.debug: print("Reduce using Args1 -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 47:
                if self.debug: print("Reduce using Args1 -> id comma Args1")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1] + _3)))
            elif action == 44:
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
            elif action == 49:
                if self.debug: print("Reduce using E -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 42:
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
                self.stack.append((gt,(('=', _2, _4))))
            elif action == 51:
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
            elif action == 40:
                if self.debug: print("Reduce using E -> minus E")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(('-', _2))))
            elif action == 50:
                if self.debug: print("Reduce using E -> number")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 41:
                if self.debug: print("Reduce using E -> E del E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(('/', _1, _3))))
            elif action == 39:
                if self.debug: print("Reduce using E -> E minus E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(('-', _1, _3))))
            elif action == 37:
                if self.debug: print("Reduce using E -> E mul E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(('*', _1, _3))))
            elif action == 38:
                if self.debug: print("Reduce using E -> E plus E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(('+', _1, _3))))
            elif action == 43:
                if self.debug: print("Reduce using E -> E pow E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(('^', _1, _3))))
            elif action == 35:
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