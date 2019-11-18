'''
Created on 01.12.2017

--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input), but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take, starting by going down onto the only line connected to the top of the diagram. It needs to follow this path until it reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction, and only turn left or right when there's no other option. In addition, someone has left letters on the line; these also don't change its direction, but it can use them to keep track of where it's been. For example:

     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 

Given this diagram, the packet needs to take the following path:

    Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward to the first +.
    Travel right, up, and right, passing through B in the process.
    Continue down (collecting C), right, and up (collecting D).
    Finally, go all the way left through E and stopping at F.

Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What letters will it see (in the order it would see them) if it follows the path? (The routing diagram is very wide; make sure you view it without line wrapping.)

'''
import unittest
from tools.vector import Vector2d

class Test(unittest.TestCase):
    testdata=['     |          ',
                  '     |  +--+    ',
                  '     A  |  C    ',
                  ' F---|----E|--+ ',
                  '     |  |  |  D ',
                  '     +B-+  +--+ ',
                  ]
    def testPartOne(self):
        
        self.assertEqual(solve(self.testdata), 'ABCDEF')
    def testPartTwo(self):
        
        self.assertEqual(solvePartTwo(self.testdata), 38)

def solve(input_list):
    t = Turtle(input_list)
    t.run()
    return t.output_str
    
class Turtle(object):
    def __init__(self, routing_diagram):
        self.map=routing_diagram[:]
        self.north = Vector2d(0,-1)
        self.south = Vector2d(0,1)
        self.east = Vector2d(1,0)
        self.west = Vector2d(-1,0)
        self.pos = Vector2d(routing_diagram[0].index('|'),0)
        self.dir = self.south
        self.output_str=''
        self.running = True
        self.step_count = 0
        
    def run(self):
        while self.running:
            self.pos += self.dir
            route_symbol=self.getSymbol(self.pos)
            self.step_count += 1
            if route_symbol.isalpha():
                self.output_str+=route_symbol
            
            elif route_symbol == '|':
                if self.dir==self.east or self.dir==self.west:
                    lookahead=self.pos + self.dir
                    next_symbol= self.getSymbol(lookahead)
                    if next_symbol!='-' and not next_symbol.isalpha():
                        print "oops"
                        pass#turn
                        
            elif route_symbol == '+':
                if self.dir==self.north or self.dir==self.south:
                    lookahead=self.pos + self.east
                    next_symbol= self.getSymbol(lookahead)
                    if next_symbol=='-' or next_symbol.isalpha():
                        self.dir = self.east
                    else:
                        self.dir = self.west
                else:
                    lookahead=self.pos + self.north
                    next_symbol= self.getSymbol(lookahead)
                    if next_symbol=='|' or next_symbol.isalpha():
                        self.dir = self.north
                    else:
                        self.dir = self.south
                        
            elif route_symbol == '-':
                if self.dir==self.north or self.dir==self.south:
                    lookahead = self.pos + self.dir
                    next_symbol= self.getSymbol(lookahead)
                    if next_symbol!='|' and not next_symbol.isalpha():
                        print "oops"
                        pass#turn
            
            elif route_symbol == ' ':
                self.running = False
        

    def getSymbol(self,position):
        return self.map[position.y][position.x]

def solvePartTwo(input_list):
    t = Turtle(input_list)
    t.run()
    return t.step_count
            
enableUnitTest = False


if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:           
            puzzleInput = inFile.read().rstrip()
            print solve(puzzleInput.split('\n'))
            print solvePartTwo(puzzleInput.split('\n'))