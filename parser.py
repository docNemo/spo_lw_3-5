from lexer import *
from enum import IntEnum
from collections import deque


from classes import *


def stateToString(state):
  return [ ".","%eof","SS","comma","doublep","id","Args1","Type","comma","Args1Call","E","assign","id","let","E","typeFloat","lparen","rparen","typeFun","Type","Types","typeInt","semicol","S","SS","comma","Type","Types","Args1","Args1Call","lparen","rparen","E","A","D","E","mul","E","E","E","E","E","E","E","plus","minus","del","pow","id","lparen","rparen","ArgsCall","float","int","minus","assign","func","id","lparen","rparen","Args" ][state]

def expectedSym(state):
  return [ "SS","%eof","%eof","Args1","Type/Type","doublep/doublep","rparen","comma/rparen","Args1Call","rparen","comma/rparen/mul/plus/minus/del/pow","E","assign","id","%eof/semicol/mul/plus/minus/del/pow","comma/rparen","Types","typeFun","Type","comma/rparen","rparen","comma/rparen","SS","semicol/%eof","%eof","Types","comma/rparen","rparen","rparen","rparen","E","%eof/comma/del/minus/mul/plus/pow/rparen/semicol","rparen/mul/plus/minus/del/pow","%eof/semicol","%eof/semicol","%eof/semicol/mul/plus/minus/del/pow","E","mul/%eof/comma/del/minus/mul/plus/pow/rparen/semicol/plus/minus/del/pow","mul/plus/%eof/comma/del/minus/mul/plus/pow/rparen/semicol/minus/del/pow","mul/plus/minus/%eof/comma/del/minus/mul/plus/pow/rparen/semicol/del/pow","mul/plus/minus/del/%eof/comma/del/minus/mul/plus/pow/rparen/semicol/pow","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen/semicol","mul/plus/minus/del/pow/%eof/comma/del/minus/mul/plus/pow/rparen/semicol","mul/plus/minus/del/pow/%eof/semicol","E","E","E","E","lparen/%eof/comma/del/minus/mul/plus/pow/rparen/semicol","ArgsCall","%eof/comma/del/minus/mul/plus/pow/rparen/semicol","rparen","%eof/comma/del/minus/mul/plus/pow/rparen/semicol","%eof/comma/del/minus/mul/plus/pow/rparen/semicol","E","E","id","lparen","Args","assign","rparen" ][state]

class Parser:
    Action = [
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,13,61,56,61,61],
        [62,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [1,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,61,61,61,61,61,61,61,61,61,61,61,5,61,61,61,61,61,61,61],
        [61,16,61,61,61,61,61,61,61,61,61,61,61,61,61,61,21,61,15,61],
        [61,61,61,61,61,61,61,61,4,61,61,61,61,61,61,61,61,61,61,61],
        [61,61,63,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,61,64,61,61,3,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [61,61,65,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,61,66,36,44,8,45,46,61,61,61,47,61,61,61,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [61,61,61,61,61,61,61,61,61,61,11,61,61,61,61,61,61,61,61,61],
        [61,61,61,61,61,61,61,61,61,61,61,61,12,61,61,61,61,61,61,61],
        [67,61,61,36,44,61,45,46,61,67,61,47,61,61,61,61,61,61,61,61],
        [61,61,68,61,61,68,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,16,69,61,61,61,61,61,61,61,61,61,61,61,61,61,21,61,15,61],
        [61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,18],
        [61,16,61,61,61,61,61,61,61,61,61,61,61,61,61,61,21,61,15,61],
        [61,61,70,61,61,70,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,61,17,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,61,71,61,61,71,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,13,61,56,61,61],
        [72,61,61,61,61,61,61,61,61,22,61,61,61,61,61,61,61,61,61,61],
        [73,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,16,69,61,61,61,61,61,61,61,61,61,61,61,61,61,21,61,15,61],
        [61,61,74,61,61,25,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,61,75,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,61,76,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,61,77,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [78,61,78,78,78,78,78,78,61,78,61,78,61,61,61,61,61,61,61,61],
        [61,61,31,36,44,61,45,46,61,61,61,47,61,61,61,61,61,61,61,61],
        [79,61,61,61,61,61,61,61,61,79,61,61,61,61,61,61,61,61,61,61],
        [80,61,61,61,61,61,61,61,61,80,61,61,61,61,61,61,61,61,61,61],
        [81,61,61,36,44,61,45,46,61,81,61,47,61,61,61,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [82,61,82,82,82,82,82,82,61,82,61,47,61,61,61,61,61,61,61,61],
        [83,61,83,36,83,83,83,46,61,83,61,47,61,61,61,61,61,61,61,61],
        [84,61,84,36,84,84,84,46,61,84,61,47,61,61,61,61,61,61,61,61],
        [85,61,85,85,85,85,85,85,61,85,61,47,61,61,61,61,61,61,61,61],
        [86,61,86,86,86,86,86,86,61,86,61,47,61,61,61,61,61,61,61,61],
        [87,61,87,87,87,87,87,87,61,87,61,87,61,61,61,61,61,61,61,61],
        [88,61,61,36,44,61,45,46,61,88,61,47,61,61,61,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [89,49,89,89,89,89,89,89,61,89,61,89,61,61,61,61,61,61,61,61],
        [61,30,90,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [91,61,91,91,91,91,91,91,61,91,61,91,61,61,61,61,61,61,61,61],
        [61,61,50,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [92,61,92,92,92,92,92,92,61,92,61,92,61,61,61,61,61,61,61,61],
        [93,61,93,93,93,93,93,93,61,93,61,93,61,61,61,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [61,30,61,61,61,61,54,61,61,61,61,61,48,53,52,61,61,61,61,61],
        [61,61,61,61,61,61,61,61,61,61,61,61,57,61,61,61,61,61,61,61],
        [61,58,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61],
        [61,61,94,61,61,61,61,61,61,61,61,61,5,61,61,61,61,61,61,61],
        [61,61,61,61,61,61,61,61,61,61,55,61,61,61,61,61,61,61,61,61],
        [61,61,59,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61]
        ]
    GOTO = [
        [33,34,35,23,2,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,6,0,0,0,0,0],
        [0,0,0,0,0,0,7,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,10,0,0,0,0,9,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,14,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,26,0,20,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,19,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [33,34,35,23,24,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,26,0,27,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,32,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,37,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,38,0,0,0,0,0,0,0,0],
        [0,0,39,0,0,0,0,0,0,0,0],
        [0,0,40,0,0,0,0,0,0,0,0],
        [0,0,41,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,10,0,0,0,0,29,0,51,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,42,0,0,0,0,0,0,0,0],
        [0,0,43,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,28,0,0,0,0,60],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0]
        ]
    def __init__(self, debug=False):
        self.debug = debug
    def parse(self, tokens):
        stack = deque()
        def top():
            if len(stack)>0:
                return stack[-1][0]
            else:
                return 0
        a = next(tokens)
        while True:
            action = self.Action[top()][int(a[0])]
            if action == 62:
                stack.pop()
                return stack.pop()[1]
            elif action == 67:
                if self.debug: print("Reduce using A -> let id assign E")
                _4 = stack.pop()[1]
                _3 = stack.pop()[1][1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][0] # A
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(Assign(_2, _4))))
            elif action == 94:
                if self.debug: print("Reduce using Args -> ")
                
                gt = self.GOTO[top()][10] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(tuple())))
            elif action == 76:
                if self.debug: print("Reduce using Args -> Args1")
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][10] # Args
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(_1)))
            elif action == 64:
                if self.debug: print("Reduce using Args1 -> id doublep Type")
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][5] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,((Param(_1, _3),))))
            elif action == 63:
                if self.debug: print("Reduce using Args1 -> id doublep Type comma Args1")
                _5 = stack.pop()[1]
                _4 = stack.pop()[1][1]
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][5] # Args1
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,((Param(_1, _3), *_5))))
            elif action == 66:
                if self.debug: print("Reduce using Args1Call -> E")
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][7] # Args1Call
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,((_1,))))
            elif action == 65:
                if self.debug: print("Reduce using Args1Call -> E comma Args1Call")
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][7] # Args1Call
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,((_1, *_3))))
            elif action == 90:
                if self.debug: print("Reduce using ArgsCall -> ")
                
                gt = self.GOTO[top()][9] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(tuple())))
            elif action == 77:
                if self.debug: print("Reduce using ArgsCall -> Args1Call")
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][9] # ArgsCall
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(_1)))
            elif action == 88:
                if self.debug: print("Reduce using D -> func id lparen Args rparen assign E")
                _7 = stack.pop()[1]
                _6 = stack.pop()[1][1]
                _5 = stack.pop()[1][1]
                _4 = stack.pop()[1]
                _3 = stack.pop()[1][1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][1] # D
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(makeF(_2, _4, _7))))
            elif action == 92:
                if self.debug: print("Reduce using E -> float")
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(make(Float, _1))))
            elif action == 89:
                if self.debug: print("Reduce using E -> id")
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(make(Id, _1))))
            elif action == 91:
                if self.debug: print("Reduce using E -> id lparen ArgsCall rparen")
                _4 = stack.pop()[1][1]
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(make(Call, _1, _3))))
            elif action == 93:
                if self.debug: print("Reduce using E -> int")
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(make(Int, _1))))
            elif action == 78:
                if self.debug: print("Reduce using E -> lparen E rparen")
                _3 = stack.pop()[1][1]
                _2 = stack.pop()[1]
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(_2)))
            elif action == 87:
                if self.debug: print("Reduce using E -> minus E")
                _2 = stack.pop()[1]
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(make(UnaryOp, '-', _2))))
            elif action == 85:
                if self.debug: print("Reduce using E -> E del E")
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(make(BinaryOp, '/', _1, _3))))
            elif action == 84:
                if self.debug: print("Reduce using E -> E minus E")
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(make(BinaryOp, '-', _1, _3))))
            elif action == 82:
                if self.debug: print("Reduce using E -> E mul E")
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(make(BinaryOp, '*', _1, _3))))
            elif action == 83:
                if self.debug: print("Reduce using E -> E plus E")
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(make(BinaryOp, '+', _1, _3))))
            elif action == 86:
                if self.debug: print("Reduce using E -> E pow E")
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][2] # E
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(make(BinaryOp,'^', _1, _3))))
            elif action == 79:
                if self.debug: print("Reduce using S -> A")
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][3] # S
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(clearObjects(_1))))
            elif action == 80:
                if self.debug: print("Reduce using S -> D")
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][3] # S
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(clearObjects(_1))))
            elif action == 81:
                if self.debug: print("Reduce using S -> E")
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][3] # S
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(clearObjects(_1))))
            elif action == 72:
                if self.debug: print("Reduce using SS -> S")
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][4] # SS
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,([_1])))
            elif action == 73:
                if self.debug: print("Reduce using SS -> S semicol SS")
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][4] # SS
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,([_1, *_3])))
            elif action == 70:
                if self.debug: print("Reduce using Type -> lparen Types rparen typeFun Type")
                _5 = stack.pop()[1]
                _4 = stack.pop()[1][1]
                _3 = stack.pop()[1][1]
                _2 = stack.pop()[1]
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][6] # Type
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(FunctionType(_2, _5))))
            elif action == 68:
                if self.debug: print("Reduce using Type -> typeFloat")
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][6] # Type
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(FloatType())))
            elif action == 71:
                if self.debug: print("Reduce using Type -> typeInt")
                _1 = stack.pop()[1][1]
                gt = self.GOTO[top()][6] # Type
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,(IntType())))
            elif action == 69:
                if self.debug: print("Reduce using Types -> ")
                
                gt = self.GOTO[top()][8] # Types
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,([])))
            elif action == 74:
                if self.debug: print("Reduce using Types -> Type")
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][8] # Types
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,([_1])))
            elif action == 75:
                if self.debug: print("Reduce using Types -> Type comma Types")
                _3 = stack.pop()[1]
                _2 = stack.pop()[1][1]
                _1 = stack.pop()[1]
                gt = self.GOTO[top()][8] # Types
                if gt==0: raise Exception("No goto")
                if self.debug:
                    print(f'{top()} is now on top of the stack;')
                    print(f'{gt} will be placed on the stack')
                stack.append((gt,([_1, *_3])))
            elif action == 61:
                lastSt = top()
                parsed=stateToString(lastSt)
                while len(stack) > 0:
                    stack.pop()
                    parsed = stateToString(top()) + " " + parsed
                raise Exception(
                  f'Rejection state reached after parsing "{parsed}", when encoutered symbol "{a[0].name}" in state {lastSt}. Expected "{expectedSym(lastSt)}"')
            else:
                if self.debug: print(f"Shift to {action}")
                stack.append((action, a))
                a=next(tokens)