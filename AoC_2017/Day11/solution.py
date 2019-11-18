'''
Created on 01.12.2017

--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need to determine the fewest number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

For example:

    ne,ne,ne is 3 steps away.
    ne,ne,sw,sw is 0 steps away (back where you started).
    ne,ne,s,s is 2 steps away (se,se).
    se,sw,se,sw,sw is 3 steps away (s,s,sw).

'''
import unittest


class Test(unittest.TestCase):
    def testHexDistance(self):
        test_data = [['ne,ne,ne', 3],
                     ['ne,ne,sw,sw', 0],
                     ['ne,ne,s,s', 2],
                     ['se,sw,se,sw,sw', 3],
                     ]
                      
        for data, expectation in test_data:
            actual = solve(data)
            self.assertEqual(actual, expectation,"Data: " + data + "\nExpected: " + str(expectation)+"\nActual: " + str(actual))


def solve(input_string):
    delta_lookup = {'ne':[1,0,-1],
                    'se':[0,1,-1],
                    's':[-1,1,0],
                    'sw':[-1,0,1],
                    'nw':[0,-1,1],
                    'n':[1,-1,0]
                    }
    pos = [0,0,0]
    max_distance=0
    for direction in input_string.split(','):
        pos = map(lambda x,y:x+y, pos, delta_lookup[direction])
        max_distance=max(max_distance,abs(max(pos, key=abs)))
    return abs(max(pos, key=abs))

def solvePartTwo(input_string):
    delta_lookup = {'ne':[1,0,-1],
                    'se':[0,1,-1],
                    's':[-1,1,0],
                    'sw':[-1,0,1],
                    'nw':[0,-1,1],
                    'n':[1,-1,0]
                    }
    pos = [0,0,0]
    max_distance=0
    for direction in input_string.split(','):
        pos = map(lambda x,y:x+y, pos, delta_lookup[direction])
        max_distance=max(max_distance,abs(max(pos, key=abs)))
    return max_distance
                
            
enableUnitTest = False

if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            puzzleInput = inFile.read().rstrip()        
            print solve(puzzleInput)
            print solvePartTwo(puzzleInput)
    