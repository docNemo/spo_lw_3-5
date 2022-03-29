from lexer import *
from enum import IntEnum
from collections import deque



def stateToString(state):
  return [ ".","%eof","E","mul","E","E","E","E","E","E","E","E","E","plus","minus","minus","del","assign","id","pow","assign","lparen","rparen","Args","id","comma","Args1","Args1","number","lparen","rparen" ][state]

def expectedSym(state):
  return [ "E","%eof","%eof/mul/plus/minus/del/pow","E","mul/%eof/del/minus/mul/plus/pow/rparen/plus/minus/del/pow","mul/plus/%eof/del/minus/mul/plus/pow/rparen/minus/del/pow","mul/plus/minus/%eof/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/%eof/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/del/%eof/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/%eof/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/pow/%eof/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/rparen","E","E","E","E","E","assign/lparen/%eof/del/minus/mul/plus/pow/rparen","E","E","Args","assign","rparen","rparen/comma","Args1","rparen","rparen","%eof/del/minus/mul/plus/pow/rparen","E","%eof/del/minus/mul/plus/pow/rparen" ][state]

class Parser:
    Action = [
        [31,29,31,31,31,31,15,31,31,31,18,28],
        [32,31,31,31,31,31,31,31,31,31,31,31],
        [1,31,31,3,13,31,14,16,31,19,31,31],
        [31,29,31,31,31,31,15,31,31,31,18,28],
        [33,31,33,33,33,31,33,33,31,19,31,31],
        [34,31,34,3,34,31,34,16,31,19,31,31],
        [35,31,35,3,35,31,35,16,31,19,31,31],
        [36,31,36,36,36,31,36,36,31,36,31,31],
        [37,31,37,37,37,31,37,37,31,19,31,31],
        [38,31,38,3,13,31,14,16,31,19,31,31],
        [39,31,39,39,39,31,39,39,31,19,31,31],
        [40,31,40,3,13,31,14,16,31,19,31,31],
        [31,31,30,3,13,31,14,16,31,19,31,31],
        [31,29,31,31,31,31,15,31,31,31,18,28],
        [31,29,31,31,31,31,15,31,31,31,18,28],
        [31,29,31,31,31,31,15,31,31,31,18,28],
        [31,29,31,31,31,31,15,31,31,31,18,28],
        [31,29,31,31,31,31,15,31,31,31,18,28],
        [41,21,41,41,41,31,41,41,17,41,31,31],
        [31,29,31,31,31,31,15,31,31,31,18,28],
        [31,29,31,31,31,31,15,31,31,31,18,28],
        [31,31,42,31,31,31,31,31,31,31,24,31],
        [31,31,31,31,31,31,31,31,20,31,31,31],
        [31,31,22,31,31,31,31,31,31,31,31,31],
        [31,31,43,31,31,25,31,31,31,31,31,31],
        [31,31,31,31,31,31,31,31,31,31,24,31],
        [31,31,44,31,31,31,31,31,31,31,31,31],
        [31,31,45,31,31,31,31,31,31,31,31,31],
        [46,31,46,46,46,31,46,46,31,46,31,31],
        [31,29,31,31,31,31,15,31,31,31,18,28],
        [47,31,47,47,47,31,47,47,31,47,31,31]
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
        [10,0,0],
        [11,0,0],
        [0,23,27],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,26],
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
            if action == 32:
                self.stack.pop()
                return self.stack.pop()[1]
            elif action == 42:
                if self.debug: print("Reduce using Args -> ")
                
                gt = self.GOTO[self.top()][1] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 45:
                if self.debug: print("Reduce using Args -> Args1")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][1] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 43:
                if self.debug: print("Reduce using Args1 -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 44:
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
            elif action == 41:
                if self.debug: print("Reduce using E -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 38:
                if self.debug: print("Reduce using E -> id assign E")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(('=', _1, _3))))
            elif action == 40:
                if self.debug: print("Reduce using E -> id lparen Args rparen assign E")
                _6 = self.stack.pop()[1]
                _5 = self.stack.pop()[1][1]
                _4 = self.stack.pop()[1][1]
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,((_1, _3, _6))))
            elif action == 47:
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
            elif action == 36:
                if self.debug: print("Reduce using E -> minus E")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(('-', _2))))
            elif action == 46:
                if self.debug: print("Reduce using E -> number")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 37:
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
            elif action == 35:
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
            elif action == 33:
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
            elif action == 34:
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
            elif action == 39:
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
            elif action == 31:
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