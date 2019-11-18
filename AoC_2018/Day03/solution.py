'''
Created on 03.12.2017

--- Day 3: No Matter How You Slice It ---
'''

import unittest
import re
import numpy as np

class Test(unittest.TestCase):
    def testOverlapOnce(self):
        self.assertEqual(solve('#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 5,5: 2x2\n'), 4)
        
    def testOverlapTwice(self):
        self.assertEqual(solve('#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 4,4: 3x3\n'), 8)
        
    def testOverlapTwiceExact(self):
        self.assertEqual(solve('#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 3,3: 2x2\n'), 4)
        
fabric = np.zeros((1000,1000))
pattern = re.compile(r".*?(\d+),(\d+): (\d+)x(\d+)")   

def solve(claims):
    for claim in claims.splitlines():
        m = pattern.match(claim)
        x,y,w,h = list(map(int,m.groups()))
        fabric[x:x+w,y:y+h] += 1
    return np.sum(fabric > 1)

def solvePartTwo(claims):
    for claim in claims.splitlines():
        m = pattern.match(claim)
        x,y,w,h = list(map(int,m.groups()))
        if np.all(fabric[x:x+w,y:y+h] == 1):
            return claim

if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read()
        print(solve(puzzleInput))
        print(solvePartTwo(puzzleInput))

    