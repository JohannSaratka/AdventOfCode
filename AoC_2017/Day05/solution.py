'''
Created on 01.12.2017

--- Day 5: A Maze of Twisty Trampolines, All Alike ---

Part One
The message includes a list of the offsets for each jump. Jumps are relative: -1 moves 
to the previous instruction, and 2 skips the next one. Start at the first instruction in 
the list. The goal is to follow the jumps until one leads outside the list.

In addition, these instructions are a little strange; after each jump, the offset of that 
instruction increases by 1. So, if you come across an offset of 3, you would move three 
instructions forward, but change it to a 4 for the next time it is encountered.

For example, consider the following list of jump offsets:

0
3
0
1
-3

Positive jumps ("forward") move downward; negative jumps move upward. For legibility in 
this example, these offset values will be written all on one line, with the current 
instruction marked in parentheses. The following steps would be taken before an exit 
is found:

    (0) 3  0  1  -3  - before we have taken any steps.
    (1) 3  0  1  -3  - jump with offset 0 (that is, don't jump at all). Fortunately, the instruction is then incremented to 1.
     2 (3) 0  1  -3  - step forward because of the instruction we just modified. The first instruction is incremented again, now to 2.
     2  4  0  1 (-3) - jump all the way to the end; leave a 4 behind.
     2 (4) 0  1  -2  - go back to where we just were; increment -3 to -2.
     2  5  0  1  -2  - jump 4 steps forward, escaping the maze.

In this example, the exit is reached in 5 steps.

How many steps does it take to reach the exit?

Part Two
Now, the jumps are even stranger: after each jump, if the offset was three or more, 
instead decrease it by 1. Otherwise, increase it by 1 as before.

Using this rule with the above example, the process now takes 10 steps, and the 
offset values after finding the exit are left as 2 3 2 3 -1.

How many steps does it now take to reach the exit?
'''
import unittest


class Test(unittest.TestCase):
    def testOne(self):
        self.assertEqual(solve('0\n3\n0\n1\n-3'), 5)
    def testTwo(self):
        self.assertEqual(solvePartTwo('0\n3\n0\n1\n-3'), 10)   
def solve(input_list):
    jump_offsets = map(int,input_list.split())
    isEnd = False
    pos=0
    n=0
    while not isEnd:
        jump = jump_offsets[pos]
        jump_offsets[pos] += 1
        pos+=jump
        isEnd = (pos >= len(jump_offsets))        
        n+=1
    return n

def solvePartTwo(input_list):
    jump_offsets = map(int,input_list.split())
    isEnd = False
    pos=0
    n=0
    while not isEnd:
        jump = jump_offsets[pos]
        if jump>=3:
            jump_offsets[pos] -= 1
        else:
            jump_offsets[pos] += 1
        pos+=jump
        isEnd = (pos >= len(jump_offsets))        
        n+=1
    return n

enableUnitTest = False

if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            puzzleInput = inFile.read().rstrip()
            print solve(puzzleInput),                
            print solvePartTwo(puzzleInput)
    