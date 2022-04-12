from lexer import *
from enum import IntEnum
from collections import deque



def stateToString(state):
  return [ ".","%eof","E","mul","E","E","E","E","E","E","E","E","E","plus","minus","minus","del","assign","id","let","pow","id","lparen","rparen","Args","assign","func","id","lparen","rparen","Args","id","number","comma","comma","Args1","Args1","Args1","number","lparen","rparen" ][state]

def expectedSym(state):
  return [ "E","%eof","%eof/mul/plus/minus/del/pow","E","mul/%eof/del/minus/mul/plus/pow/rparen/plus/minus/del/pow","mul/plus/%eof/del/minus/mul/plus/pow/rparen/minus/del/pow","mul/plus/minus/%eof/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/%eof/del/minus/mul/plus/pow/rparen/del/pow","mul/plus/minus/del/%eof/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/%eof/del/minus/mul/plus/pow/rparen/pow","mul/plus/minus/del/pow/%eof/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/%eof/del/minus/mul/plus/pow/rparen","mul/plus/minus/del/pow/rparen","E","E","E","E","E","assign","id","E","lparen/%eof/del/minus/mul/plus/pow/rparen","Args","%eof/del/minus/mul/plus/pow/rparen","rparen","E","id","lparen","Args","assign","rparen","rparen/comma","rparen/comma","Args1","Args1","rparen","rparen","rparen","%eof/del/minus/mul/plus/pow/rparen","E","%eof/del/minus/mul/plus/pow/rparen" ][state]

class Parser:
    Action = [
        [41,39,41,41,41,41,15,41,41,41,21,38,19,26],
        [42,41,41,41,41,41,41,41,41,41,41,41,41,41],
        [1,41,41,3,13,41,14,16,41,20,41,41,41,41],
        [41,39,41,41,41,41,15,41,41,41,21,38,19,26],
        [43,41,43,43,43,41,43,43,41,20,41,41,41,41],
        [44,41,44,3,44,41,44,16,41,20,41,41,41,41],
        [45,41,45,3,45,41,45,16,41,20,41,41,41,41],
        [46,41,46,46,46,41,46,46,41,46,41,41,41,41],
        [47,41,47,47,47,41,47,47,41,20,41,41,41,41],
        [48,41,48,3,13,41,14,16,41,20,41,41,41,41],
        [49,41,49,49,49,41,49,49,41,20,41,41,41,41],
        [50,41,50,3,13,41,14,16,41,20,41,41,41,41],
        [41,41,40,3,13,41,14,16,41,20,41,41,41,41],
        [41,39,41,41,41,41,15,41,41,41,21,38,19,26],
        [41,39,41,41,41,41,15,41,41,41,21,38,19,26],
        [41,39,41,41,41,41,15,41,41,41,21,38,19,26],
        [41,39,41,41,41,41,15,41,41,41,21,38,19,26],
        [41,39,41,41,41,41,15,41,41,41,21,38,19,26],
        [41,41,41,41,41,41,41,41,17,41,41,41,41,41],
        [41,41,41,41,41,41,41,41,41,41,18,41,41,41],
        [41,39,41,41,41,41,15,41,41,41,21,38,19,26],
        [51,22,51,51,51,41,51,51,41,51,41,41,41,41],
        [41,41,52,41,41,41,41,41,41,41,31,32,41,41],
        [53,41,53,53,53,41,53,53,41,53,41,41,41,41],
        [41,41,23,41,41,41,41,41,41,41,41,41,41,41],
        [41,39,41,41,41,41,15,41,41,41,21,38,19,26],
        [41,41,41,41,41,41,41,41,41,41,27,41,41,41],
        [41,28,41,41,41,41,41,41,41,41,41,41,41,41],
        [41,41,52,41,41,41,41,41,41,41,31,32,41,41],
        [41,41,41,41,41,41,41,41,25,41,41,41,41,41],
        [41,41,29,41,41,41,41,41,41,41,41,41,41,41],
        [41,41,54,41,41,33,41,41,41,41,41,41,41,41],
        [41,41,55,41,41,34,41,41,41,41,41,41,41,41],
        [41,41,41,41,41,41,41,41,41,41,31,32,41,41],
        [41,41,41,41,41,41,41,41,41,41,31,32,41,41],
        [41,41,56,41,41,41,41,41,41,41,41,41,41,41],
        [41,41,57,41,41,41,41,41,41,41,41,41,41,41],
        [41,41,58,41,41,41,41,41,41,41,41,41,41,41],
        [59,41,59,59,59,41,59,59,41,59,41,41,41,41],
        [41,39,41,41,41,41,15,41,41,41,21,38,19,26],
        [60,41,60,60,60,41,60,60,41,60,41,41,41,41]
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
        [0,24,37],
        [0,0,0],
        [0,0,0],
        [11,0,0],
        [0,0,0],
        [0,0,0],
        [0,30,37],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,35],
        [0,0,36],
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
            if action == 42:
                self.stack.pop()
                return self.stack.pop()[1]
            elif action == 52:
                if self.debug: print("Reduce using Args -> ")
                
                gt = self.GOTO[self.top()][1] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(None)))
            elif action == 58:
                if self.debug: print("Reduce using Args -> Args1")
                _1 = self.stack.pop()[1]
                gt = self.GOTO[self.top()][1] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 54:
                if self.debug: print("Reduce using Args1 -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 56:
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
            elif action == 55:
                if self.debug: print("Reduce using Args1 -> number")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1])))
            elif action == 57:
                if self.debug: print("Reduce using Args1 -> number comma Args1")
                _3 = self.stack.pop()[1]
                _2 = self.stack.pop()[1][1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][2] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,([_1] + _3)))
            elif action == 50:
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
            elif action == 51:
                if self.debug: print("Reduce using E -> id")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 53:
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
            elif action == 48:
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
            elif action == 60:
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
            elif action == 46:
                if self.debug: print("Reduce using E -> minus E")
                _2 = self.stack.pop()[1]
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(('-', _2))))
            elif action == 59:
                if self.debug: print("Reduce using E -> number")
                _1 = self.stack.pop()[1][1]
                gt = self.GOTO[self.top()][0] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{self.top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                self.stack.append((gt,(_1)))
            elif action == 47:
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
            elif action == 45:
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
            elif action == 43:
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
            elif action == 44:
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
            elif action == 49:
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
            elif action == 41:
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