from lexer import *
from enum import IntEnum
from collections import deque



def stateToString(state):
  return [ ".","%eof","E","mul","E","E","E","E","E","E","E","E","E","plus","minus","minus","del","assign","id","let","pow","id","lparen","rparen","Args","assign","func","id","lparen","rparen","Args","id","comma","Args1","Args1","number","lparen","rparen" ][state]

def expectedSym(state):
  return [ "E","%eof","%eof/mul/plus/minus/del/pow","E","mul/%eof/del/minus/mul/plus/pow/rparen/plus/minus/del/pow","mul/plus/%eof/del/minus/mul/plus/pow/rparen/minus/del/pow","mul/plus/minus/%eof/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/%eof/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/del/%eof/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/%eof/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/pow/%eof/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/rparen","E","E","E","E","E","assign","id","E","lparen/%eof/del/minus/mul/plus/pow/rparen","Args","%eof/del/minus/mul/plus/pow/rparen","rparen","E","id","lparen","Args","assign","rparen","rparen/comma","Args1","rparen","rparen","%eof/del/minus/mul/plus/pow/rparen","E","%eof/del/minus/mul/plus/pow/rparen" ][state]

class Parser:
    Action = [
        [38,36,38,38,38,38,15,38,38,38,21,35,19,26],
        [39,38,38,38,38,38,38,38,38,38,38,38,38,38],
        [1,38,38,3,13,38,14,16,38,20,38,38,38,38],
        [38,36,38,38,38,38,15,38,38,38,21,35,19,26],
        [40,38,40,40,40,38,40,40,38,20,38,38,38,38],
        [41,38,41,3,41,38,41,16,38,20,38,38,38,38],
        [42,38,42,3,42,38,42,16,38,20,38,38,38,38],
        [43,38,43,43,43,38,43,43,38,43,38,38,38,38],
        [44,38,44,44,44,38,44,44,38,20,38,38,38,38],
        [45,38,45,3,13,38,14,16,38,20,38,38,38,38],
        [46,38,46,46,46,38,46,46,38,20,38,38,38,38],
        [47,38,47,3,13,38,14,16,38,20,38,38,38,38],
        [38,38,37,3,13,38,14,16,38,20,38,38,38,38],
        [38,36,38,38,38,38,15,38,38,38,21,35,19,26],
        [38,36,38,38,38,38,15,38,38,38,21,35,19,26],
        [38,36,38,38,38,38,15,38,38,38,21,35,19,26],
        [38,36,38,38,38,38,15,38,38,38,21,35,19,26],
        [38,36,38,38,38,38,15,38,38,38,21,35,19,26],
        [38,38,38,38,38,38,38,38,17,38,38,38,38,38],
        [38,38,38,38,38,38,38,38,38,38,18,38,38,38],
        [38,36,38,38,38,38,15,38,38,38,21,35,19,26],
        [48,22,48,48,48,38,48,48,38,48,38,38,38,38],
        [38,38,49,38,38,38,38,38,38,38,31,38,38,38],
        [50,38,50,50,50,38,50,50,38,50,38,38,38,38],
        [38,38,23,38,38,38,38,38,38,38,38,38,38,38],
        [38,36,38,38,38,38,15,38,38,38,21,35,19,26],
        [38,38,38,38,38,38,38,38,38,38,27,38,38,38],
        [38,28,38,38,38,38,38,38,38,38,38,38,38,38],
        [38,38,49,38,38,38,38,38,38,38,31,38,38,38],
        [38,38,38,38,38,38,38,38,25,38,38,38,38,38],
        [38,38,29,38,38,38,38,38,38,38,38,38,38,38],
        [38,38,51,38,38,32,38,38,38,38,38,38,38,38],
        [38,38,38,38,38,38,38,38,38,38,31,38,38,38],
        [38,38,52,38,38,38,38,38,38,38,38,38,38,38],
        [38,38,53,38,38,38,38,38,38,38,38,38,38,38],
        [54,38,54,54,54,38,54,54,38,54,38,38,38,38],
        [38,36,38,38,38,38,15,38,38,38,21,35,19,26],
        [55,38,55,55,55,38,55,55,38,55,38,38,38,38]
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
        [0,0,0],
        [0,24,34],
        [0,0,0],
        [0,0,0],
        [11,0,0],
        [0,0,0],
        [0,0,0],
        [0,30,34],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,33],
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
            if action == 39:
                self.stack.pop()
                return self.stack.pop()[1]
            elif action == 49:
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
                if self.debug: print("Reduce using Args1 -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 52:
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
            elif action == 47:
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
            elif action == 48:
                if self.debug: print("Reduce using E -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 50:
                if self.debug: print("Reduce using E -> id lparen Args rparen")
                _4 = self.stack.pop()[1][1]
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,((_1, _3))))
            elif action == 45:
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
            elif action == 43:
                if self.debug: print("Reduce using E -> minus E")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(('-', _2))))
            elif action == 54:
                if self.debug: print("Reduce using E -> number")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 44:
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
            elif action == 42:
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
            elif action == 40:
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
            elif action == 41:
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
            elif action == 46:
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
            elif action == 38:
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