'''
Created on 03.12.2017

--- Day 3: No Matter How You Slice It ---
'''

import unittest
from datetime import datetime
import numpy as np
import operator

class Test(unittest.TestCase):
    testinput = ("dabAcCaCBAcCcaDA")
    def testFirstStrategy(self):   
        self.assertEqual(solve(self.testinput), 10)
        
    def testSecondStrategy(self):   
        self.assertEqual(solvePartTwo(self.testinput), 4455)

def solve(polymer):
    polymer = list(polymer.strip())
    i=0
    while(i<len(polymer)-1):    
        if polymer[i].swapcase()==polymer[i+1]:
            del polymer[i]
            del polymer[i]
            i -= 2
        i+=1
    return len(polymer)
        
def solvePartTwo(timetable):
    pass

if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read()
        print(solve(puzzleInput))
        print(solvePartTwo(puzzleInput))

    